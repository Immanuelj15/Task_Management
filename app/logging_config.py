import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(log_level: int = logging.INFO, log_dir: str = "logs") -> None:
    """
    Configures structured logging for console and rotating file output.
    Ensures log directory exists.
    """
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    log_file = Path(log_dir) / "app.log"

    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s:%(lineno)d] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Avoid duplicate handlers if setup_logging is called multiple times
    if not any(isinstance(h, RotatingFileHandler) for h in root_logger.handlers):
        file_handler = RotatingFileHandler(
            filename=str(log_file),
            maxBytes=1_000_000,  # 1 MB
            backupCount=3,
            encoding="utf-8",
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(log_level)
        root_logger.addHandler(file_handler)

    if not any(isinstance(h, logging.StreamHandler) and not isinstance(h, RotatingFileHandler) for h in root_logger.handlers):
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(log_level)
        root_logger.addHandler(console_handler)


def get_logger(name: str) -> logging.Logger:
    """Convenience getter for named loggers."""
    return logging.getLogger(name)


# Initialize logging on module load
setup_logging()
logger = get_logger("task_management_api")
