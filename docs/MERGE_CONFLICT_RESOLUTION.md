# Git Merge Conflict Resolution Playbook & Governance (D14)

## 1. What Causes a Merge Conflict?
A merge conflict occurs when two concurrent branches modify the same line(s) of a file differently, or when one branch modifies a file while another deletes it. Git pauses the merge or rebase operation and inserts conflict markers to prompt human resolution.

---

## 2. Anatomy of a Conflict Marker

Default conflict syntax:
```text
<<<<<<< HEAD (Current branch / Target)
PORT = 8000
ENVIRONMENT = "production"
=======
PORT = 8080
ENVIRONMENT = "staging"
>>>>>>> feature/new-port (Incoming branch)
```

With `diff3` style (`git config merge.conflictstyle diff3`), the common ancestor base is also included:
```text
<<<<<<< HEAD
PORT = 8000
||||||| base
PORT = 3000
=======
PORT = 8080
>>>>>>> feature/new-port
```

---

## 3. Step-by-Step Conflict Resolution Workflow

1. **Detect Conflict Status**:
   ```bash
   git status
   # Shows "both modified: <filename>"
   ```

2. **Locate Conflict Markers**:
   Search for `<<<<<<<`, `=======`, and `>>>>>>>` across the codebase.

3. **Resolve Conflicts**:
   Manually edit the file to incorporate both intentions cleanly and eliminate all conflict markers.

4. **Verify Integrity**:
   Run the test suite to ensure the resolution did not introduce regression:
   ```bash
   pytest
   ```

5. **Stage & Finalize**:
   ```bash
   git add <resolved-files>
   git commit -m "chore(merge): resolve conflicts between main and feature-branch"
   # OR for rebase:
   git rebase --continue
   ```

---

## 4. Git Rerere (Reuse Recorded Resolution)
Enable Git to automatically remember how you resolved a conflict and apply the exact same resolution if that conflict recurs:
```bash
git config --global rerere.enabled true
```
