"""Tests for D15 Production Readiness Audit Engine."""

import pytest
from scripts.readiness_audit import (
    audit_file_structure,
    audit_security_and_secrets,
    audit_large_files,
    audit_merge_conflicts,
    audit_branch_governance,
    run_full_audit,
)


def test_audit_file_structure_passes():
    """Verify Pillar 1: Required files are present."""
    passed, message = audit_file_structure()
    assert passed is True, message


def test_audit_security_and_secrets_passes():
    """Verify Pillar 2: No secrets or real .env are tracked in git."""
    passed, message = audit_security_and_secrets()
    assert passed is True, message


def test_audit_large_files_passes():
    """Verify Pillar 3: No oversized binaries are tracked in git."""
    passed, message = audit_large_files()
    assert passed is True, message


def test_audit_merge_conflicts_passes():
    """Verify Pillar 4: Zero conflict markers exist in application code."""
    passed, message = audit_merge_conflicts()
    assert passed is True, message


def test_audit_branch_governance_passes():
    """Verify Pillar 5: Current branch conforms to naming standards."""
    passed, message = audit_branch_governance()
    assert passed is True, message


def test_run_full_audit_pillars():
    """Verify all 6 pillars are registered and evaluated in full audit."""
    results = run_full_audit()
    assert len(results) == 6
    for pillar_name, (passed, details) in results.items():
        assert isinstance(passed, bool)
        assert isinstance(details, str)
