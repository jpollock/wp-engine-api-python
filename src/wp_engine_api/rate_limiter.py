"""Rate limiter for the WP Engine API SDK."""

import time
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional

from .exceptions import RateLimitError


@dataclass
class RateLimitInfo:
    """Rate limit information for an endpoint."""

    remaining: int
    reset_time: float
    limit: int

    @classmethod
    def from_headers(cls, headers: Dict[str, str]) -> Optional["RateLimitInfo"]:
        """Create RateLimitInfo from response headers.

        Args:
            headers: Response headers from the API

        Returns:
            RateLimitInfo object if headers contain rate limit info, None otherwise
        """
        try:
            return cls(
                remaining=int(headers.get("X-RateLimit-Remaining", 0)),
                reset_time=float(headers.get("X-RateLimit-Reset", 0)),
                limit=int(headers.get("X-RateLimit-Limit", 0))
            )
        except (ValueError, TypeError):
            return None


class RateLimiter:
    """Handles rate limiting for API requests."""

    def __init__(self, max_retries: int = 3, retry_delay: float = 1.0):
        """Initialize the rate limiter.

        Args:
            max_retries: Maximum number of retry attempts
            retry_delay: Base delay between retries in seconds
        """
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._rate_limits: Dict[str, RateLimitInfo] = {}

    def update_limits(self, endpoint: str, headers: Dict[str, str]) -> None:
        """Update rate limit information from response headers.

        Args:
            endpoint: API endpoint
            headers: Response headers
        """
        rate_limit_info = RateLimitInfo.from_headers(headers)
        if rate_limit_info:
            self._rate_limits[endpoint] = rate_limit_info

    def check_limits(self, endpoint: str) -> None:
        """Check if request can proceed based on rate limits.

        Args:
            endpoint: API endpoint

        Raises:
            RateLimitError: If rate limit is exceeded
        """
        if endpoint not in self._rate_limits:
            return

        limit_info = self._rate_limits[endpoint]
        if limit_info.remaining <= 0:
            current_time = time.time()
            if current_time < limit_info.reset_time:
                wait_time = limit_info.reset_time - current_time
                raise RateLimitError(
                    f"Rate limit exceeded for endpoint {endpoint}. "
                    f"Reset in {wait_time:.1f} seconds",
                    retry_after=wait_time
                )

    def handle_rate_limit(self, endpoint: str, attempt: int = 0) -> None:
        """Handle rate limit exceeded situation.

        Args:
            endpoint: API endpoint
            attempt: Current retry attempt number

        Raises:
            RateLimitError: If max retries exceeded
        """
        if attempt >= self.max_retries:
            raise RateLimitError(
                f"Rate limit exceeded for endpoint {endpoint}. "
                f"Max retries ({self.max_retries}) exceeded."
            )

        if endpoint in self._rate_limits:
            limit_info = self._rate_limits[endpoint]
            current_time = time.time()
            if current_time < limit_info.reset_time:
                wait_time = limit_info.reset_time - current_time
                time.sleep(wait_time)
        else:
            # If we don't have rate limit info, use exponential backoff
            backoff = self.retry_delay * (2 ** attempt)
            time.sleep(backoff)

    def clear_limits(self) -> None:
        """Clear all stored rate limit information."""
        self._rate_limits.clear()
