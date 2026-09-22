from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Generic, TypeVar

T = TypeVar("T")


@dataclass
class PipelineContext(Generic[T]):
    """
    Encapsulates state, payload, and metadata passed through pipeline stages.
    Demonstrates OOP encapsulation and generics.
    """
    payload: T
    metadata: dict[str, Any] = field(default_factory=dict)
    history: list[dict[str, Any]] = field(default_factory=list)
    aborted: bool = False
    abort_reason: str | None = None

    def abort(self, reason: str) -> None:
        """Abort execution of subsequent pipeline stages."""
        self.aborted = True
        self.abort_reason = reason

    def record_stage(self, stage_name: str, details: str = "") -> None:
        """Record stage completion in execution history."""
        self.history.append({
            "stage": stage_name,
            "timestamp": datetime.utcnow().isoformat(),
            "details": details,
        })


class PipelineStage(ABC, Generic[T]):
    """
    Abstract Base Class defining the contract for pipeline processing stages.
    Demonstrates OOP Abstraction and Polymorphism.
    """

    @property
    def stage_name(self) -> str:
        return self.__class__.__name__

    @abstractmethod
    def process(self, context: PipelineContext[T]) -> PipelineContext[T]:
        """
        Process the given pipeline context and return updated context.
        Must be implemented by concrete subclass stages.
        """
        pass


class Pipeline(Generic[T]):
    """
    Pipeline orchestrator that executes an ordered sequence of stages.
    Demonstrates the Pipeline Design Pattern.
    """

    def __init__(self, stages: list[PipelineStage[T]] | None = None) -> None:
        self._stages: list[PipelineStage[T]] = stages or []

    def add_stage(self, stage: PipelineStage[T]) -> "Pipeline[T]":
        """Method chaining to append a stage to the pipeline."""
        self._stages.append(stage)
        return self

    def execute(self, initial_payload: T, metadata: dict[str, Any] | None = None) -> PipelineContext[T]:
        """Execute all stages sequentially, halting early if context is aborted."""
        context = PipelineContext(
            payload=initial_payload,
            metadata=metadata or {},
        )

        for stage in self._stages:
            if context.aborted:
                break
            context = stage.process(context)
            context.record_stage(stage.stage_name)

        return context
