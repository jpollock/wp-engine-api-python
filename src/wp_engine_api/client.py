"""Main client for the WP Engine API SDK."""

from typing import Optional, Union

from wp_engine_api.generated import Configuration
from wp_engine_api.generated.api_client import ApiClient
from wp_engine_api.generated.api import (
    AccountApi,
    AccountUserApi,
    BackupApi,
    CacheApi,
    DomainApi,
    InstallApi,
    SiteApi,
    SshKeyApi,
    StatusApi,
    UserApi,
)

from .config import Config
from .endpoints import (
    AccountsEndpoint,
    BackupsEndpoint,
    DomainsEndpoint,
    InstallsEndpoint,
    SitesEndpoint,
    SshKeysEndpoint,
    UsersEndpoint,
)
from .rate_limiter import RateLimiter


class WPEngineAPI:
    """Main WP Engine API client."""

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        config: Optional[Union[Config, dict]] = None,
        **kwargs
    ):
        """Initialize the WP Engine API client.

        There are several ways to provide authentication credentials:
        1. Pass username and password directly
        2. Set WP_ENGINE_API_USERNAME and WP_ENGINE_API_PASSWORD environment variables
        3. Create a .env file with these variables
        4. Pass a Config object or dict with credentials

        Args:
            username: API username (optional if using env vars or config)
            password: API password (optional if using env vars or config)
            config: Configuration object or dict (optional)
            **kwargs: Additional configuration options
        """
        # Initialize configuration
        if username and password:
            self.config = Config(username=username, password=password, **kwargs)
        elif isinstance(config, dict):
            self.config = Config.from_env(**{**config, **kwargs})
        elif isinstance(config, Config):
            self.config = config
        else:
            self.config = Config.from_env(**kwargs)

        self.config.validate()

        # Initialize rate limiter
        self.rate_limiter = RateLimiter(
            max_retries=self.config.max_retries,
            retry_delay=self.config.retry_delay
        )

        # Initialize API client
        configuration = Configuration(
            host=self.config.base_url,
            username=self.config.username,
            password=self.config.password,
        )
        
        self.api_client = ApiClient(configuration)

        # Initialize API instances
        self._account_api = AccountApi(self.api_client)
        self._account_user_api = AccountUserApi(self.api_client)
        self._backup_api = BackupApi(self.api_client)
        self._cache_api = CacheApi(self.api_client)
        self._domain_api = DomainApi(self.api_client)
        self._install_api = InstallApi(self.api_client)
        self._site_api = SiteApi(self.api_client)
        self._ssh_key_api = SshKeyApi(self.api_client)
        self._status_api = StatusApi(self.api_client)
        self._user_api = UserApi(self.api_client)

        # Initialize endpoint handlers
        self._accounts = None
        self._backups = None
        self._domains = None
        self._installs = None
        self._sites = None
        self._ssh_keys = None
        self._users = None

    @property
    def accounts(self) -> AccountsEndpoint:
        """Get accounts endpoint handler."""
        if self._accounts is None:
            self._accounts = AccountsEndpoint(
                self._account_api,
                self._account_user_api,
                self.rate_limiter
            )
        return self._accounts

    @property
    def backups(self) -> BackupsEndpoint:
        """Get backups endpoint handler."""
        if self._backups is None:
            self._backups = BackupsEndpoint(
                self._backup_api,
                self.rate_limiter
            )
        return self._backups

    @property
    def domains(self) -> DomainsEndpoint:
        """Get domains endpoint handler."""
        if self._domains is None:
            self._domains = DomainsEndpoint(
                self._domain_api,
                self.rate_limiter
            )
        return self._domains

    @property
    def installs(self) -> InstallsEndpoint:
        """Get installs endpoint handler."""
        if self._installs is None:
            self._installs = InstallsEndpoint(
                self._install_api,
                self._cache_api,
                self.rate_limiter
            )
        return self._installs

    @property
    def sites(self) -> SitesEndpoint:
        """Get sites endpoint handler."""
        if self._sites is None:
            self._sites = SitesEndpoint(
                self._site_api,
                self.rate_limiter
            )
        return self._sites

    @property
    def ssh_keys(self) -> SshKeysEndpoint:
        """Get SSH keys endpoint handler."""
        if self._ssh_keys is None:
            self._ssh_keys = SshKeysEndpoint(
                self._ssh_key_api,
                self.rate_limiter
            )
        return self._ssh_keys

    @property
    def users(self) -> UsersEndpoint:
        """Get users endpoint handler."""
        if self._users is None:
            self._users = UsersEndpoint(
                self._user_api,
                self.rate_limiter
            )
        return self._users
