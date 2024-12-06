"""Common test configuration and fixtures."""

import os
import pytest

@pytest.fixture(autouse=True)
def setup_test_env():
    """Set up test environment variables."""
    # Save original environment
    original_env = dict(os.environ)
    
    # Clean any existing WP Engine API environment variables
    for key in list(os.environ.keys()):
        if key.startswith('WP_ENGINE_API_'):
            del os.environ[key]
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)

@pytest.fixture
def mock_env_credentials(monkeypatch):
    """Mock environment credentials for testing."""
    monkeypatch.setenv('WP_ENGINE_API_USERNAME', 'test-user')
    monkeypatch.setenv('WP_ENGINE_API_PASSWORD', 'test-pass')
    monkeypatch.setenv('WP_ENGINE_API_URL', 'https://test-api.wpengineapi.com/v1')
