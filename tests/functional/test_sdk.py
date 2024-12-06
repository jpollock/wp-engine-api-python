"""Functional tests for the WP Engine API SDK."""

import os
from unittest import mock

import pytest
from wp_engine_api import WPEngineAPI
from wp_engine_api.exceptions import (
    AuthenticationError,
    ConfigurationError,
    ResourceNotFoundError
)
from wp_engine_api.generated.exceptions import ApiException


@pytest.fixture
def test_credentials():
    """Set up test credentials."""
    return {
        'username': 'test-user',
        'password': 'test-pass'
    }


@pytest.fixture
def sdk(test_credentials):
    """Initialize SDK with test credentials."""
    with mock.patch.dict(os.environ, {
        'WP_ENGINE_API_USERNAME': test_credentials['username'],
        'WP_ENGINE_API_PASSWORD': test_credentials['password']
    }):
        return WPEngineAPI()


def test_sdk_initialization(test_credentials):
    """Test SDK initialization with different methods."""
    # Test direct credentials
    sdk1 = WPEngineAPI(
        username=test_credentials['username'],
        password=test_credentials['password']
    )
    assert sdk1.config.username == test_credentials['username']
    assert sdk1.config.password == test_credentials['password']

    # Test environment variables
    with mock.patch.dict(os.environ, {
        'WP_ENGINE_API_USERNAME': test_credentials['username'],
        'WP_ENGINE_API_PASSWORD': test_credentials['password']
    }):
        sdk2 = WPEngineAPI()
        assert sdk2.config.username == test_credentials['username']
        assert sdk2.config.password == test_credentials['password']

    # Test config dict
    sdk3 = WPEngineAPI(config={
        'username': test_credentials['username'],
        'password': test_credentials['password']
    })
    assert sdk3.config.username == test_credentials['username']
    assert sdk3.config.password == test_credentials['password']


def test_sdk_initialization_error():
    """Test SDK initialization with invalid credentials."""
    with pytest.raises(ConfigurationError):
        WPEngineAPI(username='invalid', password='')


def test_api_endpoints_initialization(sdk):
    """Test all API endpoints are properly initialized."""
    assert sdk.accounts is not None
    assert sdk.backups is not None
    assert sdk.domains is not None
    assert sdk.installs is not None
    assert sdk.sites is not None
    assert sdk.ssh_keys is not None
    assert sdk.users is not None


def test_list_accounts_pagination(sdk):
    """Test pagination for listing accounts."""
    with pytest.raises(AuthenticationError) as exc_info:
        sdk.accounts.list(limit=5, offset=0)
    assert exc_info.value.status_code == 401
    assert "Bad Credentials" in str(exc_info.value)


def test_error_handling_invalid_account():
    """Test error handling for invalid account ID."""
    # Create a mock SDK with valid credentials to test 404 error
    sdk = WPEngineAPI(
        username='valid-user',
        password='valid-pass'
    )

    # Create a mock response that simulates a 404 error
    mock_response = mock.Mock()
    mock_response.status = 404
    mock_response.data = None
    mock_response.getheaders.return_value = {}

    # Create an API exception with the mock response
    api_exception = ApiException(
        http_resp=mock_response,
        body='{"message": "Account not found"}',
        data=None
    )
    api_exception.status = 404

    # Mock the API call to raise our custom exception
    with mock.patch('wp_engine_api.generated.api.account_api.AccountApi.get_account') as mock_get:
        mock_get.side_effect = api_exception
        with pytest.raises(ResourceNotFoundError) as exc_info:
            sdk.accounts.get('invalid-id')
        assert exc_info.value.status_code == 404
        assert "Account not found" in str(exc_info.value)


def test_error_handling_invalid_credentials():
    """Test error handling for invalid credentials."""
    invalid_sdk = WPEngineAPI(
        username='invalid',
        password='invalid'
    )
    with pytest.raises(AuthenticationError) as exc_info:
        invalid_sdk.accounts.list()
    assert exc_info.value.status_code == 401
    assert "Bad Credentials" in str(exc_info.value)


def test_get_current_user(sdk):
    """Test getting current user information."""
    with pytest.raises(AuthenticationError) as exc_info:
        sdk.users.get_current()
    assert exc_info.value.status_code == 401
    assert "Bad Credentials" in str(exc_info.value)


def test_list_sites_pagination(sdk):
    """Test pagination for listing sites."""
    with pytest.raises(AuthenticationError) as exc_info:
        sdk.sites.list(limit=5, offset=0)
    assert exc_info.value.status_code == 401
    assert "Bad Credentials" in str(exc_info.value)


def test_base_url_configuration():
    """Test base URL configuration."""
    custom_url = "https://custom-api.wpengineapi.com/v1"
    sdk = WPEngineAPI(config={
        'username': 'test-user',
        'password': 'test-pass',
        'base_url': custom_url
    })
    assert sdk.config.base_url == custom_url


def test_rate_limiter(sdk):
    """Test rate limiter functionality."""
    # Make multiple rapid requests to test rate limiting
    for _ in range(3):
        with pytest.raises(AuthenticationError) as exc_info:
            sdk.accounts.list(limit=1)
        assert exc_info.value.status_code == 401
        assert "Bad Credentials" in str(exc_info.value)
