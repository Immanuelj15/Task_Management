import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

EnvironmentType = Literal["development", "testing", "staging", "production"]


def load_dotenv(filepath: str | Path | None = None) -> bool:
    """
    Lightweight, dependency-free .env file loader.
    Loads key-value pairs into os.environ if not already present.
    """
    if filepath is None:
        # Look for .env in current working directory and project root
        candidates = [
            Path(".env"),
            Path(__file__).resolve().parent.parent / ".env",
        ]
        for candidate in candidates:
            if candidate.is_file():
                filepath = candidate
                break

    if not filepath or not Path(filepath).is_file():
        return False

    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if "=" in stripped:
                key, val = stripped.split("=", 1)
                key = key.strip()
                val = val.strip().strip("\"'")
                if key and key not in os.environ:
                    os.environ[key] = val
    return True


# Automatically attempt to load .env on import
load_dotenv()


def _get_bool(key: str, default: bool = False) -> bool:
    val = os.getenv(key)
    if val is None:
        return default
    return val.strip().lower() in ("true", "1", "t", "yes", "y")


def _get_int(key: str, default: int) -> int:
    val = os.getenv(key)
    if val is None:
        return default
    try:
        return int(val.strip())
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "Task Management API")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    ENVIRONMENT: EnvironmentType = os.getenv("ENVIRONMENT", "development")  # type: ignore
    DEBUG: bool = _get_bool("DEBUG", True)
    HOST: str = os.getenv("HOST", "127.0.0.1")
    PORT: int = _get_int("PORT", 8000)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default-dev-secret-key-replace-in-prod")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    DEFAULT_PAGE_LIMIT: int = _get_int("DEFAULT_PAGE_LIMIT", 100)

    def __post_init__(self) -> None:
        if not (1 <= self.PORT <= 65535):
            raise ValueError(f"Invalid PORT {self.PORT}. Must be between 1 and 65535.")
        if self.ENVIRONMENT not in ("development", "testing", "staging", "production"):
            raise ValueError(
                f"Invalid ENVIRONMENT '{self.ENVIRONMENT}'. Allowed: development, testing, staging, production."
            )

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

    @property
    def is_development(self) -> bool:
        return self.ENVIRONMENT == "development"

    @property
    def is_testing(self) -> bool:
        return self.ENVIRONMENT == "testing"


def get_settings() -> Settings:
    """Factory function to build settings with current environment."""
    return Settings()


settings = get_settings()

