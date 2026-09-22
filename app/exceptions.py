from typing import Any


class BaseAppException(ValueError):
    """Base domain exception for all application errors, inheriting from ValueError."""

    def __init__(
        self,
        message: str,
        error_code: str = "APPLICATION_ERROR",
        status_code: int = 400,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}



class EntityNotFoundException(BaseAppException):
    """Exception raised when a requested resource is not found."""

    def __init__(self, entity_name: str, entity_id: Any) -> None:
        super().__init__(
            message=f"{entity_name} with id '{entity_id}' not found",
            error_code=f"{entity_name.upper()}_NOT_FOUND",
            status_code=404,
            details={"entity": entity_name, "id": entity_id},
        )


class UserNotFoundException(EntityNotFoundException):
    def __init__(self, user_id: Any) -> None:
        super().__init__("User", user_id)


class TaskNotFoundException(EntityNotFoundException):
    def __init__(self, task_id: Any) -> None:
        super().__init__("Task", task_id)


class DuplicateResourceException(BaseAppException):
    """Exception raised when an entity already exists with identical unique attributes."""

    def __init__(self, message: str, error_code: str = "DUPLICATE_RESOURCE") -> None:
        super().__init__(message=message, error_code=error_code, status_code=400)


class UserAlreadyExistsException(DuplicateResourceException):
    def __init__(self, field: str, value: str) -> None:
        super().__init__(
            message=f"{field.capitalize()} '{value}' is already taken.",
            error_code="USER_ALREADY_EXISTS",
        )


class AuthenticationException(BaseAppException):
    """Exception raised when authentication fails."""

    def __init__(self, message: str = "Invalid username or password") -> None:
        super().__init__(message=message, error_code="INVALID_CREDENTIALS", status_code=401)


class ValidationAppException(BaseAppException):
    """Exception raised for business rule validation failures."""

    def __init__(self, message: str) -> None:
        super().__init__(message=message, error_code="VALIDATION_FAILED", status_code=400)
