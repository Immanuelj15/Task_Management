"""Production Readiness Audit Engine (D15).

Executes a comprehensive 6-pillar audit against the repository to verify
compliance, security, testing integrity, and operational readiness before
production deployment.
"""

import os
import subprocess
import sys
from typing import Dict, List, Tuple

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

REQUIRED_PROJECT_FILES = [
    ".gitignore",
    ".gitattributes",
    ".env.example",
    "README.md",
    "requirements.txt",
    "pytest.ini",
    "app/main.py",
    "app/config.py",
    "docs/GIT_BRANCHING_STRATEGY.md",
    "docs/GIT_LARGE_FILES.md",
    "docs/CODE_REVIEW_GUIDELINES.md",
    "docs/MERGE_CONFLICT_RESOLUTION.md",
    "docs/PRODUCTION_READINESS_AUDIT.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/workflows/ci.yml",
]


def audit_file_structure() -> Tuple[bool, str]:
    """Pillar 1: Verify presence of all critical production files."""
    missing = [f for f in REQUIRED_PROJECT_FILES if not os.path.exists(f)]
    if missing:
        return False, f"Missing required files: {', '.join(missing)}"
    return True, f"All {len(REQUIRED_PROJECT_FILES)} critical files present."


def audit_security_and_secrets() -> Tuple[bool, str]:
    """Pillar 2: Verify no secrets or real .env file is tracked in git."""
    try:
        res = subprocess.run(
            ["git", "ls-files"],
            capture_output=True,
            text=True,
            check=True,
        )
        tracked = res.stdout.splitlines()
        forbidden = [".env", "id_rsa", ".pem", ".key"]
        leaked = [f for f in tracked if any(f.endswith(pat) for pat in forbidden)]
        if leaked:
            return False, f"Sensitive files tracked in git: {', '.join(leaked)}"
        return True, "No secrets, keys, or .env files tracked in Git."
    except Exception as exc:
        return False, f"Git check failed: {exc}"


def audit_large_files() -> Tuple[bool, str]:
    """Pillar 3: Verify no tracked files exceed the 5 MB limit."""
    try:
        from scripts.check_large_files import get_tracked_files, check_file_sizes
        tracked = get_tracked_files()
        violations, _ = check_file_sizes(tracked)
        if violations:
            return False, f"Found {len(violations)} files exceeding 5MB size limit."
        return True, f"All {len(tracked)} tracked files comply with size threshold."
    except Exception as exc:
        return False, f"Large file audit failed: {exc}"


def audit_merge_conflicts() -> Tuple[bool, str]:
    """Pillar 4: Verify zero unresolved merge conflict markers exist in source."""
    try:
        from scripts.merge_conflict_simulator import scan_directory_for_conflicts
        conflicts = scan_directory_for_conflicts("app")
        if conflicts:
            return False, f"Unresolved conflict markers in {len(conflicts)} files."
        return True, "Zero merge conflict markers found in application code."
    except Exception as exc:
        return False, f"Conflict audit failed: {exc}"


def audit_branch_governance() -> Tuple[bool, str]:
    """Pillar 5: Verify branch naming standards."""
    try:
        from scripts.validate_branch_name import get_current_branch, validate_branch_name
        current = get_current_branch()
        if not validate_branch_name(current):
            return False, f"Current branch '{current}' violates naming conventions."
        return True, f"Branch '{current}' satisfies governance policy."
    except Exception as exc:
        return False, f"Branch audit failed: {exc}"


def audit_automated_tests(skip_recursive: bool = True) -> Tuple[bool, str]:
    """Pillar 6: Run full pytest suite (excluding recursive test runner)."""
    try:
        cmd = [sys.executable, "-m", "pytest", "-q", "--tb=no"]
        if skip_recursive:
            cmd.extend(["-k", "not test_readiness_audit"])
        res = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60,
        )
        if res.returncode == 0:
            return True, "All automated tests executed and passed (100% green)."
        return False, f"Pytest failed with exit code {res.returncode}:\n{res.stdout[-300:]}"
    except Exception as exc:
        return False, f"Test suite run failed: {exc}"


def run_full_audit(skip_recursive_tests: bool = True) -> Dict[str, Tuple[bool, str]]:
    """Execute all 6 readiness audit pillars."""
    return {
        "1. File Structure & Completeness": audit_file_structure(),
        "2. Security & Secrets Hygiene": audit_security_and_secrets(),
        "3. Large Files & LFS Compliance": audit_large_files(),
        "4. Merge Conflict Cleanliness": audit_merge_conflicts(),
        "5. Git Branching Governance": audit_branch_governance(),
        "6. Automated Test Suite (Pytest)": audit_automated_tests(skip_recursive=skip_recursive_tests),
    }


def main() -> int:
    print("=" * 70)
    print("   TASK MANAGEMENT API - PRODUCTION READINESS AUDIT (D15)")
    print("=" * 70)

    results = run_full_audit(skip_recursive_tests=True)
    passed_count = sum(1 for passed, _ in results.values() if passed)
    total_count = len(results)

    for pillar, (passed, details) in results.items():
        status = "[PASS]" if passed else "[FAIL]"
        print(f"\n{status} {pillar}")
        print(f"       -> {details}")

    print("\n" + "=" * 70)
    print(f"SUMMARY: {passed_count}/{total_count} Pillars Passed ({passed_count / total_count * 100:.1f}%)")
    print("=" * 70)

    if passed_count == total_count:
        print("\n[RESULT] SYSTEM IS 100% PRODUCTION READY FOR DEPLOYMENT! (READY)\n")
        return 0
    else:
        print("\n[RESULT] AUDIT FAILED. Resolve blocking items before deployment.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())

