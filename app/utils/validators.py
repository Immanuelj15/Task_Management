import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


def validate_email_format(email: str) -> bool:
    """Validate that the given string is a valid email format."""
    if not email or not isinstance(email, str):
        return False
    return bool(EMAIL_REGEX.match(email.strip()))


def validate_username(username: str) -> tuple[bool, str]:
    """Validate username length and characters."""
    if not username:
        return False, "Username cannot be empty."
    clean = username.strip()
    if len(clean) < 3:
        return False, "Username must be at least 3 characters long."
    if len(clean) > 30:
        return False, "Username must not exceed 30 characters."
    if not re.match(r"^[a-zA-Z0-9_]+$", clean):
        return False, "Username can only contain letters, numbers, and underscores."
    return True, ""


def validate_task_status(status: str) -> bool:
    """Validate task status against allowed values."""
    valid_statuses = {"todo", "in_progress", "completed"}
    return status.lower() in valid_statuses
