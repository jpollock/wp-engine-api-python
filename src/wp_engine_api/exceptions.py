"""Exceptions for the WP Engine API SDK."""

import functools
from typing import Any, Callable, TypeVar

from wp_engine_api.generated.exceptions import (
    ApiException,
    ApiValueError,
    ApiTypeError,
)
from wp_engine_api.generated.models import (
    AuthenticationErrorResponse,
    BadRequestErrorResponse,
    ForbiddenErrorResponse,
    NotFoundErrorResponse,
)

T = TypeVar('T')

class WPEngineAPIError(Exception):
    """Base exception for WP Engine API errors."""

    def __init__(self, message: str, status_code: int = None, response: dict = None):
        """Initialize the exception.

        Args:
            message: Error message
            status_code: HTTP status code if applicable
            response: Raw API response if available
        """
        super().__init__(message)
        self.status_code = status_code
        self.response = response or {}


class ValidationError(WPEngineAPIError):
    """Raised when request validation fails."""
    pass


class AuthenticationError(WPEngineAPIError):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Authentication failed", **kwargs):
        super().__init__(message, **kwargs)


class RateLimitError(WPEngineAPIError):
    """Raised when API rate limit is exceeded."""

    def __init__(
        self,
        message: str = "Rate limit exceeded",
        retry_after: float = None,
        **kwargs
    ):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class ConfigurationError(WPEngineAPIError):
    """Raised when there's an issue with SDK configuration."""
    pass


class NetworkError(WPEngineAPIError):
    """Raised when there's a network-related error."""
    pass


class ResourceNotFoundError(WPEngineAPIError):
    """Raised when a requested resource is not found."""

    def __init__(self, message: str = "Resource not found", **kwargs):
        super().__init__(message, **kwargs)


class ServerError(WPEngineAPIError):
    """Raised when the API server returns a 5xx error."""

    def __init__(self, message: str = "Server error occurred", **kwargs):
        super().__init__(message, **kwargs)


def handle_api_error(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator to handle API errors consistently.

    Args:
        func: Function to wrap

    Returns:
        Wrapped function that handles API errors

    Raises:
        Various WPEngineAPIError subclasses based on the error
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> T:
        try:
            return func(*args, **kwargs)
        except ApiException as e:
            status_code = getattr(e, 'status', None)
            response = None

            try:
                response = e.body
            except (AttributeError, ValueError):
                pass

            if status_code == 401:
                raise AuthenticationError(
                    str(e),
                    status_code=status_code,
                    response=response
                )
            elif status_code == 403:
                raise AuthenticationError(
                    "Not authorized",
                    status_code=status_code,
                    response=response
                )
            elif status_code == 404:
                raise ResourceNotFoundError(
                    str(e),
                    status_code=status_code,
                    response=response
                )
            elif status_code == 429:
                retry_after = None
                if hasattr(e, 'headers') and e.headers:
                    retry_after = e.headers.get('Retry-After')
                raise RateLimitError(
                    str(e),
                    retry_after=retry_after,
                    status_code=status_code,
                    response=response
                )
            elif status_code and 500 <= status_code < 600:
                raise ServerError(
                    str(e),
                    status_code=status_code,
                    response=response
                )
            else:
                raise WPEngineAPIError(
                    str(e),
                    status_code=status_code,
                    response=response
                )
        except ApiValueError as e:
            raise ValidationError(str(e))
        except ApiTypeError as e:
            raise ValidationError(str(e))
        except Exception as e:
            if "Connection" in str(e):
                raise NetworkError(f"Network error: {str(e)}")
            raise WPEngineAPIError(str(e))

    return wrapper
