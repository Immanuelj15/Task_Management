import re
from datetime import datetime
from app.models.task import TaskPriority
from app.pipelines.base import Pipeline, PipelineContext, PipelineStage
from app.schemas.task import TaskCreate


class SanitizationStage(PipelineStage[TaskCreate]):
    """
    Stage to clean and sanitize incoming task title and description.
    Strips redundant whitespace and normalizes whitespace characters.
    """

    def process(self, context: PipelineContext[TaskCreate]) -> PipelineContext[TaskCreate]:
        payload = context.payload
        clean_title = re.sub(r"\s+", " ", payload.title).strip()
        clean_desc = re.sub(r"\s+", " ", payload.description).strip() if payload.description else ""

        # Create updated copy of TaskCreate
        updated_payload = TaskCreate(
            title=clean_title,
            description=clean_desc,
            status=payload.status,
            priority=payload.priority,
            assigned_user_id=payload.assigned_user_id,
        )
        context.payload = updated_payload
        context.metadata["sanitized"] = True
        return context


class AutoPriorityStage(PipelineStage[TaskCreate]):
    """
    Stage to intelligently infer task priority based on urgency keywords
    in title or description if priority is currently default (MEDIUM).
    """

    URGENT_KEYWORDS = {"urgent", "critical", "blocker", "emergency", "asap", "p0"}

    def process(self, context: PipelineContext[TaskCreate]) -> PipelineContext[TaskCreate]:
        payload = context.payload

        if payload.priority == TaskPriority.MEDIUM:
            text = f"{payload.title} {payload.description}".lower()
            tokens = set(re.findall(r"\b\w+\b", text))
            matched_keywords = tokens.intersection(self.URGENT_KEYWORDS)

            if matched_keywords:
                updated_payload = TaskCreate(
                    title=payload.title,
                    description=payload.description,
                    status=payload.status,
                    priority=TaskPriority.HIGH,
                    assigned_user_id=payload.assigned_user_id,
                )
                context.payload = updated_payload
                context.metadata["auto_elevated_priority"] = True
                context.metadata["matched_urgency_keywords"] = list(matched_keywords)

        return context


class AuditStage(PipelineStage[TaskCreate]):
    """
    Stage to enrich metadata with pipeline processing audit trail and timestamp.
    """

    def process(self, context: PipelineContext[TaskCreate]) -> PipelineContext[TaskCreate]:
        context.metadata["processed_at"] = datetime.utcnow().isoformat()
        context.metadata["pipeline_version"] = "1.0.0"
        return context


def build_default_task_pipeline() -> Pipeline[TaskCreate]:
    """Factory helper to build the default task ingestion pipeline."""
    return (
        Pipeline[TaskCreate]()
        .add_stage(SanitizationStage())
        .add_stage(AutoPriorityStage())
        .add_stage(AuditStage())
    )


default_task_pipeline = build_default_task_pipeline()
