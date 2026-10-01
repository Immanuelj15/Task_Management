"""Tests for D14 Merge Conflict Detection and Resolution."""

import os
import tempfile
import pytest
from scripts.merge_conflict_simulator import (
    scan_file_for_conflict_markers,
    resolve_conflict_content,
)

SAMPLE_CONFLICTED_TEXT = """\
def configure_app():
<<<<<<< HEAD
    port = 8000
    env = "production"
=======
    port = 8080
    env = "staging"
>>>>>>> feature/staging-port
    return port, env
"""


def test_scan_file_detects_conflict_markers():
    """Verify scan_file_for_conflict_markers flags lines with markers."""
    with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmp:
        tmp.write(SAMPLE_CONFLICTED_TEXT)
        tmp_path = tmp.name

    try:
        conflicts = scan_file_for_conflict_markers(tmp_path)
        assert len(conflicts) == 3
        assert any("<<<<<<<" in line for _, line in conflicts)
        assert any("=======" in line for _, line in conflicts)
        assert any(">>>>>>>" in line for _, line in conflicts)
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_scan_clean_file_returns_no_conflicts():
    """Verify clean file produces empty findings."""
    with tempfile.NamedTemporaryFile("w+", delete=False, encoding="utf-8") as tmp:
        tmp.write("def clean():\n    return 42\n")
        tmp_path = tmp.name

    try:
        conflicts = scan_file_for_conflict_markers(tmp_path)
        assert len(conflicts) == 0
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_resolve_conflict_strategy_ours():
    """Verify resolving with 'ours' picks HEAD block."""
    resolved = resolve_conflict_content(SAMPLE_CONFLICTED_TEXT, strategy="ours")
    assert "port = 8000" in resolved
    assert "env = \"production\"" in resolved
    assert "port = 8080" not in resolved
    assert "<<<<<<<" not in resolved
    assert ">>>>>>>" not in resolved


def test_resolve_conflict_strategy_theirs():
    """Verify resolving with 'theirs' picks incoming block."""
    resolved = resolve_conflict_content(SAMPLE_CONFLICTED_TEXT, strategy="theirs")
    assert "port = 8080" in resolved
    assert "env = \"staging\"" in resolved
    assert "port = 8000" not in resolved
    assert "<<<<<<<" not in resolved
    assert ">>>>>>>" not in resolved
