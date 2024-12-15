"""Configuration for the WP Engine API SDK."""

import base64
import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv

from .exceptions import ConfigurationError


@dataclass
class Config:
    """SDK configuration."""

    username: Optional[str] = None
    password: Optional[str] = None
    base_url: str = "https://api.wpengineapi.com/v1"
    max_retries: int = 3
    retry_delay: float = 1.0
    timeout: float = 30.0

    @classmethod
    def from_env(cls, **kwargs) -> "Config":
        """Create configuration from environment variables.

        Environment variables:
            WP_ENGINE_API_USERNAME: API username
            WP_ENGINE_API_PASSWORD: API password
            WP_ENGINE_API_URL: Base URL for API (optional)

        Args:
            **kwargs: Override any config values

        Returns:
            Config object

        Raises:
            ConfigurationError: If required configuration is missing
        """
        # Try to load from .env file if it exists
        load_dotenv()

        username = kwargs.get("username") or os.getenv("WP_ENGINE_API_USERNAME")
        password = kwargs.get("password") or os.getenv("WP_ENGINE_API_PASSWORD")

        if not username or not password:
            raise ConfigurationError(
                "API credentials not provided. Either:\n"
                "1. Set WP_ENGINE_API_USERNAME and WP_ENGINE_API_PASSWORD environment variables\n"
                "2. Create a .env file with these variables\n"
                "3. Pass username and password to constructor"
            )

        base_url = (
            kwargs.get("base_url")
            or os.getenv("WP_ENGINE_API_URL")
            or cls.base_url
        )

        return cls(
            username=username,
            password=password,
            base_url=base_url,
            max_retries=kwargs.get("max_retries", cls.max_retries),
            retry_delay=kwargs.get("retry_delay", cls.retry_delay),
            timeout=kwargs.get("timeout", cls.timeout),
        )

    def get_headers(self) -> dict:
        """Get headers for API requests.

        Returns:
            Dict of headers including authorization

        Raises:
            ConfigurationError: If credentials are not set
        """
        if not self.username or not self.password:
            raise ConfigurationError("API credentials not set")

        # Create basic auth header
        auth = base64.b64encode(
            f"{self.username}:{self.password}".encode()
        ).decode()

        return {
            "Authorization": f"Basic {auth}",
            "Content-Type": "application/json",
            "User-Agent": "wp-engine-api-python/0.0.1",
        }

    def validate(self) -> None:
        """Validate the configuration.

        Raises:
            ConfigurationError: If configuration is invalid
        """
        if not self.username:
            raise ConfigurationError("API username is required")
        
        if not self.password:
            raise ConfigurationError("API password is required")
        
        if not self.base_url:
            raise ConfigurationError("Base URL is required")
        
        if self.max_retries < 0:
            raise ConfigurationError("max_retries must be non-negative")
        
        if self.retry_delay < 0:
            raise ConfigurationError("retry_delay must be non-negative")
        
        if self.timeout < 0:
            raise ConfigurationError("timeout must be non-negative")
