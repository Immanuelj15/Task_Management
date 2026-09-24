import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.utils.profiler import (
    ExecutionProfiler,
    MemoryProfiler,
    get_current_memory_snapshot,
)

client = TestClient(app)


def test_memory_profiler_context():
    with MemoryProfiler() as mem:
        # Allocate a chunk of memory
        dummy_list = [i * 2 for i in range(50_000)]
        assert len(dummy_list) == 50_000

    assert mem.stats is not None
    assert mem.stats.current_kb > 0
    assert mem.stats.peak_kb > 0


def test_execution_profiler_context():
    def compute():
        total = 0
        for i in range(10_000):
            total += i
        return total

    with ExecutionProfiler(top_n=3) as prof:
        result = compute()

    assert result > 0
    assert len(prof.report) > 0
    assert "compute" in prof.report or "tottime" in prof.report


def test_get_current_memory_snapshot():
    snapshot = get_current_memory_snapshot()
    assert snapshot["tracing_active"] is True
    assert "current_allocated_kb" in snapshot
    assert "peak_allocated_kb" in snapshot


def test_api_debug_memory_endpoint():
    response = client.get("/debug/memory")
    assert response.status_code == 200
    data = response.json()
    assert data["tracing_active"] is True
    assert data["current_allocated_kb"] >= 0


def test_api_debug_profiler_tasks_endpoint():
    response = client.get("/debug/profiler/tasks")
    assert response.status_code == 200
    data = response.json()
    assert "tasks_returned" in data
    assert "memory_stats" in data
    assert "top_hotspots_snippet" in data


def test_api_debug_system_endpoint():
    response = client.get("/debug/system")
    assert response.status_code == 200
    data = response.json()
    assert "python_version" in data
    assert "platform" in data
    assert "active_threads" in data
    assert data["active_threads"] >= 1
