import cProfile
import io
import pstats
import sys
import tracemalloc
from dataclasses import dataclass
from typing import Any, Callable, Generator


@dataclass
class MemoryStats:
    current_kb: float
    peak_kb: float
    delta_kb: float


class MemoryProfiler:
    """
    Context manager for measuring memory consumption of a block of code
    using Python's built-in tracemalloc module.
    """

    def __init__(self) -> None:
        self.start_memory: int = 0
        self.end_memory: int = 0
        self.peak_memory: int = 0
        self.stats: MemoryStats | None = None

    def __enter__(self) -> "MemoryProfiler":
        if not tracemalloc.is_tracing():
            tracemalloc.start()
        self.start_memory, _ = tracemalloc.get_traced_memory()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        current, peak = tracemalloc.get_traced_memory()
        self.end_memory = current
        self.peak_memory = peak
        self.stats = MemoryStats(
            current_kb=round(current / 1024, 2),
            peak_kb=round(peak / 1024, 2),
            delta_kb=round((current - self.start_memory) / 1024, 2),
        )
        return False


class ExecutionProfiler:
    """
    Context manager using standard library cProfile to analyze execution bottlenecks.
    """

    def __init__(self, top_n: int = 10) -> None:
        self.top_n = top_n
        self.profiler = cProfile.Profile()
        self.report: str = ""

    def __enter__(self) -> "ExecutionProfiler":
        self.profiler.enable()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool:
        self.profiler.disable()
        stream = io.StringIO()
        stats = pstats.Stats(self.profiler, stream=stream).sort_stats("cumulative")
        stats.print_stats(self.top_n)
        self.report = stream.getvalue()
        return False


def get_current_memory_snapshot() -> dict[str, Any]:
    """Returns real-time memory usage report from tracemalloc."""
    if not tracemalloc.is_tracing():
        tracemalloc.start()
    current, peak = tracemalloc.get_traced_memory()
    return {
        "tracing_active": tracemalloc.is_tracing(),
        "current_allocated_kb": round(current / 1024, 2),
        "peak_allocated_kb": round(peak / 1024, 2),
    }
