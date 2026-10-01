"""Tests for D13 Pull Request Governance, Templates, and CI Configuration."""

import os
import pytest


def test_pr_template_exists_and_has_required_sections():
    """Verify PR template exists and has all essential checklist sections."""
    root_dir = os.path.dirname(os.path.dirname(__file__))
    pr_template_path = os.path.join(root_dir, ".github", "PULL_REQUEST_TEMPLATE.md")
    assert os.path.exists(pr_template_path), "PULL_REQUEST_TEMPLATE.md must exist in .github/"

    with open(pr_template_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "Type of Change" in content
    assert "Engineering Quality Checklist" in content
    assert "Verification & Test Evidence" in content
    assert "Reviewer Sign-off" in content


def test_issue_templates_exist():
    """Verify issue templates exist for bugs and features."""
    root_dir = os.path.dirname(os.path.dirname(__file__))
    templates_dir = os.path.join(root_dir, ".github", "ISSUE_TEMPLATE")
    bug_report = os.path.join(templates_dir, "bug_report.md")
    feature_req = os.path.join(templates_dir, "feature_request.md")

    assert os.path.exists(bug_report), "bug_report.md must exist in .github/ISSUE_TEMPLATE/"
    assert os.path.exists(feature_req), "feature_request.md must exist in .github/ISSUE_TEMPLATE/"


def test_code_review_guidelines_exist():
    """Verify code review guidelines are documented."""
    root_dir = os.path.dirname(os.path.dirname(__file__))
    guidelines_path = os.path.join(root_dir, "docs", "CODE_REVIEW_GUIDELINES.md")
    assert os.path.exists(guidelines_path), "CODE_REVIEW_GUIDELINES.md must exist in docs/"

    with open(guidelines_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "SOLID" in content
    assert "Type Safety" in content
    assert "Security & Secrets" in content


def test_ci_workflow_exists():
    """Verify GitHub Actions CI workflow is configured."""
    root_dir = os.path.dirname(os.path.dirname(__file__))
    ci_path = os.path.join(root_dir, ".github", "workflows", "ci.yml")
    assert os.path.exists(ci_path), "ci.yml must exist in .github/workflows/"

    with open(ci_path, "r", encoding="utf-8") as f:
        content = f.read()

    assert "pytest" in content
    assert "actions/checkout" in content
