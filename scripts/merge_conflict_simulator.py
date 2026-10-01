"""Merge Conflict Simulator and Marker Scanner (D14).

Scans application source files to detect unresolved git conflict markers and
provides simulation utilities to reconcile concurrent branch divergences.
"""

import os
import re
import sys
from typing import Dict, List, Optional, Tuple

CONFLICT_START = re.compile(r"^<{7}\s*(.*)$")
CONFLICT_MID = re.compile(r"^={7}$")
CONFLICT_END = re.compile(r"^>{7}\s*(.*)$")

IGNORED_DIRS = {
    ".git",
    ".venv",
    "venv",
    "docs",
    "tests",
    "__pycache__",
    ".pytest_cache",
}


def scan_file_for_conflict_markers(file_path: str) -> List[Tuple[int, str]]:
    """Scan a given file for unresolved git conflict markers."""
    conflicts = []
    if not os.path.exists(file_path):
        return conflicts

    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for idx, line in enumerate(f, start=1):
            if (
                CONFLICT_START.match(line)
                or CONFLICT_MID.match(line)
                or CONFLICT_END.match(line)
            ):
                conflicts.append((idx, line.strip()))
    return conflicts


def scan_directory_for_conflicts(directory: str = "app") -> Dict[str, List[Tuple[int, str]]]:
    """Scan project source directory for unresolved merge conflicts."""
    findings = {}
    target_dir = directory if os.path.exists(directory) else "."
    for root, dirs, filenames in os.walk(target_dir):
        # Prune ignored directories
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]
        for fname in filenames:
            ext = os.path.splitext(fname)[1]
            if ext in {".py", ".json", ".yaml", ".yml", ".txt", ".ini", ".toml"}:
                fpath = os.path.join(root, fname)
                conflicts = scan_file_for_conflict_markers(fpath)
                if conflicts:
                    findings[fpath] = conflicts
    return findings


def resolve_conflict_content(
    conflicted_text: str, strategy: str = "ours"
) -> str:
    """Resolve conflict text programmatically using 'ours' or 'theirs' strategy."""
    lines = conflicted_text.splitlines()
    resolved_lines = []
    in_conflict = False
    in_theirs = False
    ours_block = []
    theirs_block = []

    for line in lines:
        if CONFLICT_START.match(line):
            in_conflict = True
            in_theirs = False
            ours_block = []
            theirs_block = []
            continue

        if in_conflict and CONFLICT_MID.match(line):
            in_theirs = True
            continue

        if in_conflict and CONFLICT_END.match(line):
            in_conflict = False
            if strategy == "ours":
                resolved_lines.extend(ours_block)
            elif strategy == "theirs":
                resolved_lines.extend(theirs_block)
            elif strategy == "union":
                resolved_lines.extend(ours_block)
                resolved_lines.extend(theirs_block)
            continue

        if in_conflict:
            if not in_theirs:
                ours_block.append(line)
            else:
                theirs_block.append(line)
        else:
            resolved_lines.append(line)

    return "\n".join(resolved_lines)


def main() -> int:
    print("[*] Scanning application codebase for unresolved merge conflict markers...")
    findings = scan_directory_for_conflicts("app")

    if findings:
        print("[ERROR] Unresolved merge conflict markers detected:")
        for path, markers in findings.items():
            print(f"  File: {path}")
            for line_no, marker in markers:
                print(f"    Line {line_no}: {marker}")
        return 1

    print("[OK] No unresolved merge conflict markers found in source code.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
