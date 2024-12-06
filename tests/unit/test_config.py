"""Unit tests for configuration module."""

import os
from unittest import mock

import pytest

from wp_engine_api.config import Config, ConfigurationError


@pytest.fixture
def env_vars():
    """Set up test environment variables."""
    with mock.patch.dict(os.environ, {
        'WP_ENGINE_API_USERNAME': 'test-user',
        'WP_ENGINE_API_PASSWORD': 'test-pass',
        'WP_ENGINE_API_URL': 'https://test-api.wpengineapi.com/v1'
    }):
        yield


def test_config_default_values():
    """Test default configuration values."""
    config = Config()
    assert config.username is None
    assert config.password is None
    assert config.base_url == "https://api.wpengineapi.com/v1"
    assert config.max_retries == 3
    assert config.retry_delay == 1.0
    assert config.timeout == 30.0


def test_config_custom_values():
    """Test custom configuration values."""
    config = Config(
        username="custom-user",
        password="custom-pass",
        base_url="https://custom-api.wpengineapi.com/v1",
        max_retries=5,
        retry_delay=2.0,
        timeout=60.0
    )
    assert config.username == "custom-user"
    assert config.password == "custom-pass"
    assert config.base_url == "https://custom-api.wpengineapi.com/v1"
    assert config.max_retries == 5
    assert config.retry_delay == 2.0
    assert config.timeout == 60.0


def test_config_from_env(env_vars):
    """Test configuration from environment variables."""
    config = Config.from_env()
    assert config.username == "test-user"
    assert config.password == "test-pass"
    assert config.base_url == "https://test-api.wpengineapi.com/v1"


def test_config_from_env_with_overrides(env_vars):
    """Test configuration from environment variables with overrides."""
    config = Config.from_env(
        username="override-user",
        base_url="https://override-api.wpengineapi.com/v1"
    )
    assert config.username == "override-user"
    assert config.password == "test-pass"
    assert config.base_url == "https://override-api.wpengineapi.com/v1"


def test_config_from_env_missing_credentials():
    """Test configuration error when credentials are missing."""
    with pytest.raises(ConfigurationError) as exc_info:
        Config.from_env()
    assert "API credentials not provided" in str(exc_info.value)


def test_get_headers():
    """Test header generation."""
    config = Config(username="test-user", password="test-pass")
    headers = config.get_headers()
    
    assert "Authorization" in headers
    assert headers["Authorization"].startswith("Basic ")
    assert headers["Content-Type"] == "application/json"
    assert "User-Agent" in headers


def test_get_headers_no_credentials():
    """Test header generation error when credentials are missing."""
    config = Config()
    with pytest.raises(ConfigurationError) as exc_info:
        config.get_headers()
    assert "API credentials not set" in str(exc_info.value)


def test_validate_valid_config():
    """Test validation of valid configuration."""
    config = Config(
        username="test-user",
        password="test-pass",
        base_url="https://api.wpengineapi.com/v1"
    )
    config.validate()  # Should not raise any exceptions


def test_validate_missing_username():
    """Test validation error when username is missing."""
    config = Config(password="test-pass")
    with pytest.raises(ConfigurationError) as exc_info:
        config.validate()
    assert "API username is required" in str(exc_info.value)


def test_validate_missing_password():
    """Test validation error when password is missing."""
    config = Config(username="test-user")
    with pytest.raises(ConfigurationError) as exc_info:
        config.validate()
    assert "API password is required" in str(exc_info.value)


def test_validate_invalid_max_retries():
    """Test validation error for invalid max_retries."""
    config = Config(
        username="test-user",
        password="test-pass",
        max_retries=-1
    )
    with pytest.raises(ConfigurationError) as exc_info:
        config.validate()
    assert "max_retries must be non-negative" in str(exc_info.value)


def test_validate_invalid_retry_delay():
    """Test validation error for invalid retry_delay."""
    config = Config(
        username="test-user",
        password="test-pass",
        retry_delay=-1
    )
    with pytest.raises(ConfigurationError) as exc_info:
        config.validate()
    assert "retry_delay must be non-negative" in str(exc_info.value)


def test_validate_invalid_timeout():
    """Test validation error for invalid timeout."""
    config = Config(
        username="test-user",
        password="test-pass",
        timeout=-1
    )
    with pytest.raises(ConfigurationError) as exc_info:
        config.validate()
    assert "timeout must be non-negative" in str(exc_info.value)
