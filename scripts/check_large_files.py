"""Pre-commit & CI Large File Enforcement Guard (D12).

Scans git tracked or staged files to prevent accidental commits of large
binary artifacts, local databases, or uncompressed datasets exceeding the
specified threshold.
"""

import os
import subprocess
import sys
from typing import List, Tuple

# Maximum allowed file size in bytes (5 MB)
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024

# Files or extensions allowed to be large or handled externally
ALLOWED_EXTENSIONS = {".parquet", ".onnx", ".bin"}


def get_tracked_files() -> List[str]:
    """Retrieve all files tracked by git."""
    try:
        result = subprocess.run(
            ["git", "ls-files"],
            capture_output=True,
            text=True,
            check=True,
        )
        return [f.strip() for f in result.stdout.splitlines() if f.strip()]
    except Exception:
        # Fallback to local filesystem walk if not in git context
        files = []
        for root, _, filenames in os.walk("."):
            if ".git" in root or ".venv" in root:
                continue
            for name in filenames:
                files.append(os.path.relpath(os.path.join(root, name), "."))
        return files


def check_file_sizes(
    files: List[str], max_size: int = MAX_FILE_SIZE_BYTES
) -> Tuple[List[Tuple[str, int]], List[str]]:
    """Inspect file sizes and identify violations."""
    violations = []
    missing = []
    for file_path in files:
        if not os.path.exists(file_path):
            missing.append(file_path)
            continue
        try:
            size = os.path.getsize(file_path)
            if size > max_size:
                violations.append((file_path, size))
        except OSError:
            pass
    return violations, missing


def main() -> int:
    max_mb = MAX_FILE_SIZE_BYTES / (1024 * 1024)
    print(f"[*] Scanning repository files (Max allowed size: {max_mb:.1f} MB)...")
    tracked_files = get_tracked_files()
    violations, _ = check_file_sizes(tracked_files)

    if violations:
        print("[ERROR] Found files exceeding maximum size limit:")
        for path, size in violations:
            print(f"  - {path}: {size / (1024 * 1024):.2f} MB")
        print("\nPlease track large files using Git LFS or add them to .gitignore.")
        return 1

    print(f"[OK] All {len(tracked_files)} tracked files are within the {max_mb:.1f} MB threshold.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
