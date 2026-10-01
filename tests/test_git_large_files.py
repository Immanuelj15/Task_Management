"""Tests for D12 Git Large Files and LFS Governance."""

import os
import tempfile
import pytest
from scripts.check_large_files import check_file_sizes, MAX_FILE_SIZE_BYTES


def test_gitattributes_file_exists_and_contains_lfs_rules():
    """Verify that .gitattributes is present and configures LFS rules."""
    gitattributes_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), ".gitattributes"
    )
    assert os.path.exists(gitattributes_path), ".gitattributes must be present in root"

    with open(gitattributes_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "filter=lfs" in content
    assert "*.db" in content
    assert "*.onnx" in content
    assert "*.parquet" in content
    assert "*.sqlite" in content


def test_check_file_sizes_detects_oversized_file():
    """Verify check_file_sizes flags files exceeding threshold."""
    with tempfile.NamedTemporaryFile("wb", delete=False) as tmp:
        # Create a 2KB file
        tmp.write(b"0" * 2048)
        tmp_path = tmp.name

    try:
        # Check against a small limit (1KB)
        violations, _ = check_file_sizes([tmp_path], max_size=1024)
        assert len(violations) == 1
        assert violations[0][0] == tmp_path
        assert violations[0][1] == 2048
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)


def test_check_file_sizes_accepts_compliant_files():
    """Verify check_file_sizes passes files within threshold."""
    with tempfile.NamedTemporaryFile("wb", delete=False) as tmp:
        tmp.write(b"0" * 512)
        tmp_path = tmp.name

    try:
        violations, _ = check_file_sizes([tmp_path], max_size=1024)
        assert len(violations) == 0
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
