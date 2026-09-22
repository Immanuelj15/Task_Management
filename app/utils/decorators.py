import functools
import time
from typing import Any, Callable, TypeVar

F = TypeVar("F", bound=Callable[..., Any])


def measure_time(func: F) -> F:
    """
    Decorator to measure execution time of a function.
    Attaches `last_execution_time_ms` to the function object.
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start = time.perf_counter()
        try:
            return func(*args, **kwargs)
        finally:
            elapsed_ms = (time.perf_counter() - start) * 1000
            wrapper.last_execution_time_ms = elapsed_ms  # type: ignore[attr-defined]

    wrapper.last_execution_time_ms = 0.0  # type: ignore[attr-defined]
    return wrapper  # type: ignore[return-value]


def retry(
    max_attempts: int = 3,
    delay_seconds: float = 0.01,
    exceptions: tuple[type[Exception], ...] = (Exception,),
) -> Callable[[F], F]:
    """
    Decorator that retries a function call up to max_attempts if specified exceptions occur.
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts >= max_attempts:
                        raise e
                    if delay_seconds > 0:
                        time.sleep(delay_seconds)
            return None

        return wrapper  # type: ignore[return-value]

    return decorator


def audit_action(action_name: str) -> Callable[[F], F]:
    """
    Decorator to trace domain business actions.
    Appends audit log records to an in-memory audit trail.
    """
    def decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            # Store audit invocation attribute
            invocations = getattr(wrapper, "audit_log", [])
            invocations.append({
                "action": action_name,
                "timestamp": time.time(),
            })
            setattr(wrapper, "audit_log", invocations)
            return result

        setattr(wrapper, "audit_log", [])
        return wrapper  # type: ignore[return-value]

    return decorator
