"""Data models for the WP Engine API SDK."""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from pydantic import BaseModel, Field

# Import generated models
from wp_engine_api.generated.models import (
    Account,
    AccountUser,
    Backup,
    Domain,
    DomainOrRedirect,
    Installation,
    Site,
    SshKey,
    Status,
    User,
)

# Re-export generated models
__all__ = [
    'Account',
    'AccountUser',
    'Backup',
    'Domain',
    'DomainOrRedirect',
    'Installation',
    'Site',
    'SshKey',
    'Status',
    'User',
    'Environment',
    'BackupStatus',
    'SiteStatus',
    'CacheType',
]

class Environment(str, Enum):
    """Environment types."""
    PRODUCTION = "production"
    STAGING = "staging"
    DEVELOPMENT = "development"

class BackupStatus(str, Enum):
    """Backup status types."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    FAILED = "failed"

class SiteStatus(str, Enum):
    """Site status types."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"

class CacheType(str, Enum):
    """Cache types for purging."""
    OBJECT = "object"
    PAGE = "page"
    CDN = "cdn"

# Request Models
class BackupCreate(BaseModel):
    """Backup creation request."""
    description: str = Field(..., description="A description of this backup")
    notification_emails: List[str] = Field(
        ...,
        description="The email address(es) that will receive an email once the backup has completed"
    )

class SiteCreate(BaseModel):
    """Site creation request."""
    name: str = Field(..., description="Site name")
    account_id: str = Field(..., description="Account ID")

class SiteUpdate(BaseModel):
    """Site update request."""
    name: Optional[str] = Field(None, description="Site name")

class DomainCreate(BaseModel):
    """Domain creation request."""
    name: str = Field(..., description="Domain name")
    primary: Optional[bool] = Field(None, description="Set as primary domain")
    redirect_to: Optional[str] = Field(None, description="Domain ID to redirect to")

class DomainUpdate(BaseModel):
    """Domain update request."""
    primary: Optional[bool] = Field(None, description="Set as primary domain")
    redirect_to: Optional[str] = Field(None, description="Domain ID to redirect to")

class BulkDomainCreate(BaseModel):
    """Bulk domain creation request."""
    domains: List[DomainCreate] = Field(..., min_items=1, max_items=20)

class PurgeCache(BaseModel):
    """Cache purge request."""
    type: CacheType = Field(..., description="Type of cache to purge")

class SshKeyCreate(BaseModel):
    """SSH key creation request."""
    public_key: str = Field(..., description="The public key to add")
