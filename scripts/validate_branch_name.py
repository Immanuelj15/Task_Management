"""Branch Name Validator Script for Git Branching Governance (D11).

Validates that current or supplied branch names conform to the engineering
team's branching convention.
"""

import re
import subprocess
import sys

ALLOWED_PREFIXES = (
    "feature/",
    "bugfix/",
    "hotfix/",
    "release/",
    "chore/",
    "docs/",
    "test/",
)

BRANCH_REGEX = re.compile(
    r"^(main|master|develop)$|"
    r"^(feature|bugfix|hotfix|release|chore|docs|test)/[a-z0-9._-]+$"
)


def get_current_branch() -> str:
    """Retrieve the name of the currently checked out Git branch."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()
    except Exception as exc:
        raise RuntimeError(f"Failed to detect git branch: {exc}") from exc


def validate_branch_name(branch_name: str) -> bool:
    """Validate a branch name string against the branching policy."""
    if not branch_name:
        return False
    return bool(BRANCH_REGEX.match(branch_name))


def main() -> int:
    branch = sys.argv[1] if len(sys.argv) > 1 else get_current_branch()
    print(f"[*] Validating branch: '{branch}'")

    if validate_branch_name(branch):
        print(f"[OK] Branch '{branch}' satisfies branching policy.")
        return 0
    else:
        print(
            f"[ERROR] Branch '{branch}' violates naming conventions!\n"
            f"Expected pattern: ^(feature|bugfix|hotfix|release|chore|docs|test)/[a-z0-9._-]+$\n"
            f"Allowed prefixes: {', '.join(ALLOWED_PREFIXES)}"
        )
        return 1


if __name__ == "__main__":
    sys.exit(main())
