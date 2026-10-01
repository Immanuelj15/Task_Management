# Code Review Guidelines & Engineering Rubric (D13)

## 1. Objectives
Code reviews ensure code quality, share domain knowledge across the team, prevent production bugs, and guarantee adherence to our architectural standards.

---

## 2. Review Dimensions

### A. Architectural Integrity & SOLID
- Does the code adhere to the **Single Responsibility Principle**?
- Are dependencies injected via interfaces / protocols rather than concrete classes?
- Are business logic concerns separated from transport (HTTP/FastAPI) layers?

### B. Type Safety & Validation
- Are all function arguments and returns explicitly typed?
- Does Pydantic handle incoming payload sanitization and validation?
- Are edge cases (empty strings, negative integers, null values) handled?

### C. Error Handling
- Are custom domain exceptions (`BaseAppException`) raised instead of generic `Exception`?
- Are exceptions properly translated into structured JSON responses via centralized handlers?

### D. Security & Secrets
- Ensure no sensitive credentials, API keys, or private tokens exist in commits.
- Ensure passwords are never stored in plain text (salt + SHA256 / bcrypt).

### E. Test Quality & Coverage
- Are unit tests provided for all new functions/classes?
- Do integration tests verify happy paths and failure branches?
- Is mocking used appropriately for external boundaries?

### F. Performance & Resource Management
- Are file descriptors and database connections safely closed via context managers (`with`)?
- Are memory profiler assertions satisfied for batch streaming?
