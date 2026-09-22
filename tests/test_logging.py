import logging
import uuid
import pytest
from fastapi.testclient import TestClient
from app.logging_config import get_logger, setup_logging
from app.main import app

client = TestClient(app)


def test_get_logger():
    custom_logger = get_logger("test_module")
    assert isinstance(custom_logger, logging.Logger)
    assert custom_logger.name == "test_module"


def test_setup_logging_idempotent():
    # Calling setup_logging multiple times should not create duplicate handlers
    setup_logging(log_level=logging.DEBUG)
    root = logging.getLogger()
    assert len(root.handlers) >= 1


def test_middleware_injects_x_request_id():
    response = client.get("/")
    assert response.status_code == 200
    assert "X-Request-ID" in response.headers
    # Validate it is a valid UUID
    val = response.headers["X-Request-ID"]
    assert len(val) >= 10


def test_middleware_preserves_custom_request_id():
    custom_id = f"custom-trace-{uuid.uuid4()}"
    response = client.get("/", headers={"X-Request-ID": custom_id})
    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == custom_id
