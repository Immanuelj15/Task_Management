"""Tests for D11 Git Branching Policy and Validator."""

import pytest
from scripts.validate_branch_name import validate_branch_name, ALLOWED_PREFIXES


@pytest.mark.parametrize(
    "valid_branch",
    [
        "main",
        "master",
        "develop",
        "feature/d11-branching",
        "feature/task-search",
        "bugfix/issue-104",
        "hotfix/auth-leak",
        "release/v1.0.0",
        "chore/cleanup-logs",
        "docs/api-specs",
        "test/add-e2e-tests",
    ],
)
def test_valid_branch_names(valid_branch: str):
    """Test that valid branch names conforming to standards are accepted."""
    assert validate_branch_name(valid_branch) is True


@pytest.mark.parametrize(
    "invalid_branch",
    [
        "",
        "new-feature",
        "feature/",
        "Feature/UppercasePrefix",
        "feature/has spaces in it",
        "random_branch_name",
        "hotfix/UPPERCASE_PATH",
        "wip",
    ],
)
def test_invalid_branch_names(invalid_branch: str):
    """Test that invalid branch names are rejected."""
    assert validate_branch_name(invalid_branch) is False


def test_allowed_prefixes_coverage():
    """Verify standard engineering prefixes are configured."""
    expected = {"feature/", "bugfix/", "hotfix/", "release/", "chore/", "docs/", "test/"}
    assert set(ALLOWED_PREFIXES) == expected
