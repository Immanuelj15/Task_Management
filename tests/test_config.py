import os
import tempfile
import pytest
from app.config import Settings, load_dotenv, _get_bool, _get_int


def test_default_settings():
    settings = Settings()
    assert settings.APP_NAME == "Task Management API"
    assert settings.APP_VERSION == "1.0.0"
    assert settings.ENVIRONMENT in ("development", "testing", "staging", "production")
    assert 1 <= settings.PORT <= 65535
    assert settings.DEFAULT_PAGE_LIMIT > 0


def test_custom_settings_and_profiles():
    dev_settings = Settings(ENVIRONMENT="development", PORT=8080)
    assert dev_settings.is_development is True
    assert dev_settings.is_production is False
    assert dev_settings.PORT == 8080

    prod_settings = Settings(ENVIRONMENT="production", PORT=443)
    assert prod_settings.is_production is True
    assert prod_settings.is_development is False


def test_invalid_settings_validation():
    with pytest.raises(ValueError, match="Invalid PORT"):
        Settings(PORT=70000)

    with pytest.raises(ValueError, match="Invalid ENVIRONMENT"):
        Settings(ENVIRONMENT="invalid_env")  # type: ignore


def test_helper_get_bool():
    os.environ["TEST_BOOL_TRUE"] = "yes"
    os.environ["TEST_BOOL_FALSE"] = "0"
    assert _get_bool("TEST_BOOL_TRUE", False) is True
    assert _get_bool("TEST_BOOL_FALSE", True) is False
    assert _get_bool("NON_EXISTENT_VAR", True) is True


def test_helper_get_int():
    os.environ["TEST_INT_VAL"] = "9000"
    os.environ["TEST_INT_INVALID"] = "not-a-number"
    assert _get_int("TEST_INT_VAL", 100) == 9000
    assert _get_int("TEST_INT_INVALID", 100) == 100
    assert _get_int("NON_EXISTENT_VAR", 500) == 500


def test_custom_load_dotenv():
    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".env") as tmp:
        tmp.write("# Comment line\n")
        tmp.write("TEST_ENV_KEY_1=loaded_value\n")
        tmp.write("TEST_ENV_KEY_2='quoted_value'\n")
        tmp.flush()
        tmp_name = tmp.name

    try:
        assert load_dotenv(tmp_name) is True
        assert os.environ.get("TEST_ENV_KEY_1") == "loaded_value"
        assert os.environ.get("TEST_ENV_KEY_2") == "quoted_value"
    finally:
        if os.path.exists(tmp_name):
            os.remove(tmp_name)
