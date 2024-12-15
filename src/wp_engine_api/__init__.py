"""WP Engine API Python SDK."""

from wp_engine_api.client import WPEngineAPI
from wp_engine_api.config import Config
from wp_engine_api.exceptions import (
    WPEngineAPIError,
    ValidationError,
    AuthenticationError,
    RateLimitError,
    ConfigurationError,
    NetworkError,
    ResourceNotFoundError,
    ServerError,
)
from wp_engine_api.models import (
    Account,
    AccountUser,
    Backup,
    BackupCreate,
    BackupStatus,
    BulkDomainCreate,
    CacheType,
    Domain,
    DomainCreate,
    DomainOrRedirect,
    DomainUpdate,
    Environment,
    Installation,
    PurgeCache,
    Site,
    SiteCreate,
    SiteStatus,
    SiteUpdate,
    SshKey,
    SshKeyCreate,
    Status,
    User,
)

__version__ = "0.0.1"

__all__ = [
    # Main client
    "WPEngineAPI",
    "Config",
    
    # Exceptions
    "WPEngineAPIError",
    "ValidationError",
    "AuthenticationError",
    "RateLimitError",
    "ConfigurationError",
    "NetworkError",
    "ResourceNotFoundError",
    "ServerError",
    
    # Models
    "Account",
    "AccountUser",
    "Backup",
    "BackupCreate",
    "BackupStatus",
    "BulkDomainCreate",
    "CacheType",
    "Domain",
    "DomainCreate",
    "DomainOrRedirect",
    "DomainUpdate",
    "Environment",
    "Installation",
    "PurgeCache",
    "Site",
    "SiteCreate",
    "SiteStatus",
    "SiteUpdate",
    "SshKey",
    "SshKeyCreate",
    "Status",
    "User",
]

# Version of the wp-engine-api package
__version__ = "0.0.1"
