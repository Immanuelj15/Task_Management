# Git Large File Handling & LFS Engineering Guide (D12)

## 1. The Large File Problem in Git
Git is a distributed content tracker designed for source code. Every clone downloads the complete project history. If binary files, SQLite databases, or machine learning model weights (e.g., > 10MB) are committed into a Git repository:
- The `.git` folder balloons indefinitely.
- Fetch, pull, and clone operations become painfully slow.
- Diffs between binaries are non-existent, duplicating entire binary blobs for tiny updates.

---

## 2. Mitigation Strategies

### Strategy A: Git LFS (Large File Storage)
Git LFS replaces large files (such as `.onnx`, `.pt`, `.parquet`, `.db`) with tiny text pointer files containing cryptographic hashes (SHA-256) inside the repository, while storing the actual payloads on dedicated LFS object storage servers (GitHub LFS, AWS S3, etc.).

Pointer File Structure:
```text
version https://git-lfs.github.com/spec/v1
oid sha256:4bca2801a2...
size 12458900
```

### Strategy B: Pre-commit Guard Hook
To guarantee that developers never inadvertently commit large datasets or local databases, a pre-commit check script (`scripts/check_large_files.py`) is enforced:
- Rejects any staged file exceeding **5 MB** (configurable).
- Validates that tracking attributes are enforced before push.

### Strategy C: External Artifact Storage & S3/DVC
For large ML datasets (GB/TB scale), Git should never store the data. Use:
- **DVC (Data Version Control)** coupled with AWS S3, Google Cloud Storage, or MinIO.
- Reference metadata and storage manifests inside the repository.

---

## 3. History Clean-up Protocol
If a large file was accidentally committed to Git history:
```bash
# Using git-filter-repo (recommended)
git filter-repo --path-glob '*.db' --invert-paths

# Force push the rewritten history
git push origin --force --all
```
