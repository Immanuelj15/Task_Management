# Git Branching Strategy & Governance Policy

## 1. Overview
This document defines the official Git branching model, naming conventions, and branch lifecycle policies for the **Task Management API** engineering team.

---

## 2. Branch Hierarchy

```
main (Production / Protected)
  │
  ├── release/vX.Y.Z (Staging / Release Candidates)
  │
  ├── develop (Integration branch)
  │     │
  │     ├── feature/d11-branching (Feature development)
  │     ├── bugfix/fix-user-auth  (Bug fixes)
  │     └── chore/upgrade-deps    (Maintenance & tooling)
  │
  └── hotfix/vX.Y.Z-patch (Urgent production patches directly off main)
```

### Primary Branches
- **`main`**: Represents production-ready code. Commits are strictly made via reviewed and approved Pull Requests. Direct pushes are disabled.
- **`develop`**: Default integration branch where completed features merge before staging.

### Supporting Branches
- **`feature/<short-description>`**: For new features, endpoints, or architectural modules.
- **`bugfix/<issue-id-or-description>`**: For resolving non-critical bugs found in develop/staging.
- **`hotfix/<issue-id-or-description>`**: For urgent production fixes branched from `main`.
- **`release/v<semver>`**: Preparation for a new production release (version bumps, changelog).
- **`chore/<task-description>`**: Routine maintenance, tooling, or dependency updates.

---

## 3. Branch Naming Standard
Every branch must adhere to the standard pattern:
```
^(feature|bugfix|hotfix|release|chore|docs|test)/[a-z0-9._-]+$
```

### Valid Examples:
- `feature/d11-branching`
- `feature/task-priority-scoring`
- `bugfix/fix-token-expiration`
- `hotfix/security-header-patch`
- `release/v1.2.0`
- `chore/update-requirements`

### Invalid Examples:
- `my-new-feature` (missing category prefix)
- `Feature/Task` (uppercase characters forbidden)
- `feature/task with spaces` (spaces forbidden)

---

## 4. Branch Protection Rules
For `main` and `develop`:
1. **Require pull request before merging.**
2. **Require minimum of 1 approving review.**
3. **Require status checks to pass before merging** (`pytest` must be 100% green).
4. **Require linear history** (Squash and Merge or Rebase).
5. **Delete head branch upon merge.**
