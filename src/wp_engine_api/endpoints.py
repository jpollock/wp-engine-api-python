"""API endpoint handlers for the WP Engine API SDK."""

from typing import List, Optional

from wp_engine_api.generated.api import (
    AccountApi,
    AccountUserApi,
    BackupApi,
    CacheApi,
    DomainApi,
    InstallApi,
    SiteApi,
    SshKeyApi,
    UserApi,
)
from wp_engine_api.generated.models import (
    Account,
    AccountUser,
    Backup,
    Domain,
    DomainOrRedirect,
    Installation,
    Site,
    SshKey,
    User,
)

from .exceptions import handle_api_error
from .models import (
    BackupCreate,
    BulkDomainCreate,
    DomainCreate,
    DomainUpdate,
    PurgeCache,
    SiteCreate,
    SiteUpdate,
    SshKeyCreate,
)
from .rate_limiter import RateLimiter


class BaseEndpoint:
    """Base class for API endpoints."""

    def __init__(self, rate_limiter: RateLimiter):
        """Initialize the endpoint handler.

        Args:
            rate_limiter: Rate limiter instance
        """
        self.rate_limiter = rate_limiter


class AccountsEndpoint(BaseEndpoint):
    """Handler for accounts-related endpoints."""

    def __init__(
        self,
        account_api: AccountApi,
        account_user_api: AccountUserApi,
        rate_limiter: RateLimiter
    ):
        """Initialize the accounts endpoint handler.

        Args:
            account_api: Account API instance
            account_user_api: Account user API instance
            rate_limiter: Rate limiter instance
        """
        super().__init__(rate_limiter)
        self.account_api = account_api
        self.account_user_api = account_user_api

    @handle_api_error
    def list(self, limit: int = 100, offset: int = 0) -> List[Account]:
        """List all accounts.

        Args:
            limit: Number of results per page
            offset: Offset for pagination

        Returns:
            List of Account objects
        """
        response = self.account_api.list_accounts(limit=limit, offset=offset)
        return response.results

    @handle_api_error
    def get(self, account_id: str) -> Account:
        """Get a specific account.

        Args:
            account_id: Account ID

        Returns:
            Account object
        """
        return self.account_api.get_account(account_id)

    @handle_api_error
    def list_users(self, account_id: str) -> List[AccountUser]:
        """List users for an account.

        Args:
            account_id: Account ID

        Returns:
            List of AccountUser objects
        """
        response = self.account_user_api.list_account_users(account_id)
        return response.results


class BackupsEndpoint(BaseEndpoint):
    """Handler for backups-related endpoints."""

    def __init__(self, backup_api: BackupApi, rate_limiter: RateLimiter):
        """Initialize the backups endpoint handler.

        Args:
            backup_api: Backup API instance
            rate_limiter: Rate limiter instance
        """
        super().__init__(rate_limiter)
        self.backup_api = backup_api

    @handle_api_error
    def create(self, install_id: str, data: BackupCreate) -> Backup:
        """Create a new backup.

        Args:
            install_id: Install ID
            data: Backup creation data

        Returns:
            Created Backup object
        """
        return self.backup_api.create_backup(install_id, data.dict())

    @handle_api_error
    def get(self, install_id: str, backup_id: str) -> Backup:
        """Get a specific backup.

        Args:
            install_id: Install ID
            backup_id: Backup ID

        Returns:
            Backup object
        """
        return self.backup_api.show_backup(install_id, backup_id)


class DomainsEndpoint(BaseEndpoint):
    """Handler for domains-related endpoints."""

    def __init__(self, domain_api: DomainApi, rate_limiter: RateLimiter):
        """Initialize the domains endpoint handler.

        Args:
            domain_api: Domain API instance
            rate_limiter: Rate limiter instance
        """
        super().__init__(rate_limiter)
        self.domain_api = domain_api

    @handle_api_error
    def list(self, install_id: str, limit: int = 100, offset: int = 0) -> List[Domain]:
        """List domains for an install.

        Args:
            install_id: Install ID
            limit: Number of results per page
            offset: Offset for pagination

        Returns:
            List of Domain objects
        """
        response = self.domain_api.list_domains(install_id, limit=limit, offset=offset)
        return response.results

    @handle_api_error
    def get(self, install_id: str, domain_id: str) -> Domain:
        """Get a specific domain.

        Args:
            install_id: Install ID
            domain_id: Domain ID

        Returns:
            Domain object
        """
        return self.domain_api.get_domain(install_id, domain_id)

    @handle_api_error
    def create(self, install_id: str, data: DomainCreate) -> Domain:
        """Create a new domain.

        Args:
            install_id: Install ID
            data: Domain creation data

        Returns:
            Created Domain object
        """
        return self.domain_api.create_domain(install_id, data.dict())

    @handle_api_error
    def update(self, install_id: str, domain_id: str, data: DomainUpdate) -> Domain:
        """Update a domain.

        Args:
            install_id: Install ID
            domain_id: Domain ID
            data: Domain update data

        Returns:
            Updated Domain object
        """
        return self.domain_api.update_domain(install_id, domain_id, data.dict())

    @handle_api_error
    def delete(self, install_id: str, domain_id: str) -> None:
        """Delete a domain.

        Args:
            install_id: Install ID
            domain_id: Domain ID
        """
        self.domain_api.delete_domain(install_id, domain_id)

    @handle_api_error
    def bulk_create(self, install_id: str, data: BulkDomainCreate) -> List[DomainOrRedirect]:
        """Create multiple domains.

        Args:
            install_id: Install ID
            data: Bulk domain creation data

        Returns:
            List of created Domain objects
        """
        return self.domain_api.create_bulk_domains(install_id, data.dict())


class InstallsEndpoint(BaseEndpoint):
    """Handler for installs-related endpoints."""

    def __init__(
        self,
        install_api: InstallApi,
        cache_api: CacheApi,
        rate_limiter: RateLimiter
    ):
        """Initialize the installs endpoint handler.

        Args:
            install_api: Install API instance
            cache_api: Cache API instance
            rate_limiter: Rate limiter instance
        """
        super().__init__(rate_limiter)
        self.install_api = install_api
        self.cache_api = cache_api

    @handle_api_error
    def list(
        self,
        limit: int = 100,
        offset: int = 0,
        account_id: Optional[str] = None
    ) -> List[Installation]:
        """List all installs.

        Args:
            limit: Number of results per page
            offset: Offset for pagination
            account_id: Optional account ID to filter by

        Returns:
            List of Installation objects
        """
        response = self.install_api.list_installs(
            limit=limit,
            offset=offset,
            account_id=account_id
        )
        return response.results

    @handle_api_error
    def get(self, install_id: str) -> Installation:
        """Get a specific install.

        Args:
            install_id: Install ID

        Returns:
            Installation object
        """
        return self.install_api.get_install(install_id)

    @handle_api_error
    def purge_cache(self, install_id: str, data: PurgeCache) -> None:
        """Purge cache for an install.

        Args:
            install_id: Install ID
            data: Cache purge data
        """
        self.cache_api.purge_cache(install_id, data.dict())


class SitesEndpoint(BaseEndpoint):
    """Handler for sites-related endpoints."""

    def __init__(self, site_api: SiteApi, rate_limiter: RateLimiter):
        """Initialize the sites endpoint handler.

        Args:
            site_api: Site API instance
            rate_limiter: Rate limiter instance
        """
        super().__init__(rate_limiter)
        self.site_api = site_api

    @handle_api_error
    def list(
        self,
        limit: int = 100,
        offset: int = 0,
        account_id: Optional[str] = None
    ) -> List[Site]:
        """List all sites.

        Args:
            limit: Number of results per page
            offset: Offset for pagination
            account_id: Optional account ID to filter by

        Returns:
            List of Site objects
        """
        response = self.site_api.list_sites(
            limit=limit,
            offset=offset,
            account_id=account_id
        )
        return response.results

    @handle_api_error
    def get(self, site_id: str) -> Site:
        """Get a specific site.

        Args:
            site_id: Site ID

        Returns:
            Site object
        """
        return self.site_api.get_site(site_id)

    @handle_api_error
    def create(self, data: SiteCreate) -> Site:
        """Create a new site.

        Args:
            data: Site creation data

        Returns:
            Created Site object
        """
        return self.site_api.create_site(data.dict())

    @handle_api_error
    def update(self, site_id: str, data: SiteUpdate) -> Site:
        """Update a site.

        Args:
            site_id: Site ID
            data: Site update data

        Returns:
            Updated Site object
        """
        return self.site_api.update_site(site_id, data.dict())

    @handle_api_error
    def delete(self, site_id: str) -> None:
        """Delete a site.

        Args:
            site_id: Site ID
        """
        self.site_api.delete_site(site_id)


class SshKeysEndpoint(BaseEndpoint):
    """Handler for SSH keys-related endpoints."""

    def __init__(self, ssh_key_api: SshKeyApi, rate_limiter: RateLimiter):
        """Initialize the SSH keys endpoint handler.

        Args:
            ssh_key_api: SSH key API instance
            rate_limiter: Rate limiter instance
        """
        super().__init__(rate_limiter)
        self.ssh_key_api = ssh_key_api

    @handle_api_error
    def list(self, limit: int = 100, offset: int = 0) -> List[SshKey]:
        """List all SSH keys.

        Args:
            limit: Number of results per page
            offset: Offset for pagination

        Returns:
            List of SshKey objects
        """
        response = self.ssh_key_api.list_ssh_keys(limit=limit, offset=offset)
        return response.results

    @handle_api_error
    def create(self, data: SshKeyCreate) -> SshKey:
        """Create a new SSH key.

        Args:
            data: SSH key creation data

        Returns:
            Created SshKey object
        """
        return self.ssh_key_api.create_ssh_key(data.dict())

    @handle_api_error
    def delete(self, ssh_key_id: str) -> None:
        """Delete an SSH key.

        Args:
            ssh_key_id: SSH key ID
        """
        self.ssh_key_api.delete_ssh_key(ssh_key_id)


class UsersEndpoint(BaseEndpoint):
    """Handler for users-related endpoints."""

    def __init__(self, user_api: UserApi, rate_limiter: RateLimiter):
        """Initialize the users endpoint handler.

        Args:
            user_api: User API instance
            rate_limiter: Rate limiter instance
        """
        super().__init__(rate_limiter)
        self.user_api = user_api

    @handle_api_error
    def get_current(self) -> User:
        """Get the current user.

        Returns:
            User object
        """
        return self.user_api.get_current_user()
