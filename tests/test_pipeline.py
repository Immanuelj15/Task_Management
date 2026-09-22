import pytest
from app.models.task import TaskPriority, TaskStatus
from app.pipelines.base import Pipeline, PipelineContext, PipelineStage
from app.pipelines.task_pipeline import (
    SanitizationStage,
    AutoPriorityStage,
    AuditStage,
    build_default_task_pipeline,
)
from app.schemas.task import TaskCreate
from app.services.task_service import task_service
from app.services.user_service import user_service


@pytest.fixture(autouse=True)
def clean_stores():
    user_service.clear()
    task_service.clear()
    yield
    user_service.clear()
    task_service.clear()


class DummyUppercaseStage(PipelineStage[str]):
    def process(self, context: PipelineContext[str]) -> PipelineContext[str]:
        context.payload = context.payload.upper()
        return context


class DummyAbortStage(PipelineStage[str]):
    def process(self, context: PipelineContext[str]) -> PipelineContext[str]:
        context.abort("Terminated by DummyAbortStage")
        return context


def test_base_pipeline_execution():
    pipeline = Pipeline[str]().add_stage(DummyUppercaseStage())
    result = pipeline.execute("hello world")
    assert result.payload == "HELLO WORLD"
    assert len(result.history) == 1
    assert result.history[0]["stage"] == "DummyUppercaseStage"
    assert not result.aborted


def test_base_pipeline_abort():
    pipeline = (
        Pipeline[str]()
        .add_stage(DummyAbortStage())
        .add_stage(DummyUppercaseStage())
    )
    result = pipeline.execute("hello")
    assert result.aborted is True
    assert result.abort_reason == "Terminated by DummyAbortStage"
    # DummyUppercaseStage should not have executed
    assert result.payload == "hello"


def test_sanitization_stage():
    stage = SanitizationStage()
    raw = TaskCreate(
        title="   Fix    memory   leak   ",
        description="   Multiple     spaces   in   description   ",
    )
    ctx = PipelineContext(payload=raw)
    res = stage.process(ctx)
    assert res.payload.title == "Fix memory leak"
    assert res.payload.description == "Multiple spaces in description"
    assert res.metadata["sanitized"] is True


def test_auto_priority_stage_triggers_on_urgent():
    stage = AutoPriorityStage()
    raw = TaskCreate(
        title="Fix critical server crash",
        description="Production is down",
        priority=TaskPriority.MEDIUM,
    )
    ctx = PipelineContext(payload=raw)
    res = stage.process(ctx)
    assert res.payload.priority == TaskPriority.HIGH
    assert res.metadata["auto_elevated_priority"] is True


def test_auto_priority_stage_keeps_explicit_low_priority():
    stage = AutoPriorityStage()
    raw = TaskCreate(
        title="Fix urgent server bug",
        description="Not high priority",
        priority=TaskPriority.LOW,
    )
    ctx = PipelineContext(payload=raw)
    res = stage.process(ctx)
    # Shouldn't change if user explicitly specified LOW
    assert res.payload.priority == TaskPriority.LOW
    assert "auto_elevated_priority" not in res.metadata


def test_audit_stage():
    stage = AuditStage()
    raw = TaskCreate(title="Some task")
    ctx = PipelineContext(payload=raw)
    res = stage.process(ctx)
    assert "processed_at" in res.metadata
    assert res.metadata["pipeline_version"] == "1.0.0"


def test_task_service_pipeline_integration():
    raw = TaskCreate(
        title="  Deploy   critical   security   patch   ",
        description="  ASAP    patch   ",
        priority=TaskPriority.MEDIUM,
    )
    created = task_service.create_task(raw, apply_pipeline=True)
    assert created.title == "Deploy critical security patch"
    assert created.description == "ASAP patch"
    assert created.priority == TaskPriority.HIGH
