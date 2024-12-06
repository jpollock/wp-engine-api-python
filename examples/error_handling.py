"""Error handling example for the WP Engine API Python SDK."""

from wp_engine_api import WPEngineAPI
from wp_engine_api.exceptions import (
    AuthenticationError,
    NetworkError,
    RateLimitError,
    ResourceNotFoundError,
    ValidationError,
    WPEngineAPIError,
)
from wp_engine_api.models import BackupCreate, SiteCreate, Environment

def demonstrate_authentication_error():
    """Demonstrate handling of authentication errors."""
    print("\nDemonstrating authentication error...")
    try:
        # Initialize with invalid API key
        client = WPEngineAPI(api_key="invalid_key")
        client.sites.list()
    except AuthenticationError as e:
        print(f"Authentication error caught: {e}")
        print(f"Status code: {e.status_code}")
        print(f"Response: {e.response}")

def demonstrate_resource_not_found():
    """Demonstrate handling of resource not found errors."""
    print("\nDemonstrating resource not found error...")
    try:
        client = WPEngineAPI()
        # Try to get a site with invalid ID
        client.sites.get("nonexistent_site_id")
    except ResourceNotFoundError as e:
        print(f"Resource not found error caught: {e}")
        print(f"Status code: {e.status_code}")
        print(f"Response: {e.response}")

def demonstrate_validation_error():
    """Demonstrate handling of validation errors."""
    print("\nDemonstrating validation error...")
    try:
        client = WPEngineAPI()
        # Try to create a site with invalid data
        invalid_site_data = SiteCreate(
            name="",  # Invalid: empty name
            environment="invalid_env",  # Invalid: not a valid environment
            php_version="invalid"  # Invalid: not a valid PHP version
        )
        client.sites.create(invalid_site_data)
    except ValidationError as e:
        print(f"Validation error caught: {e}")

def demonstrate_rate_limit_error():
    """Demonstrate handling of rate limit errors."""
    print("\nDemonstrating rate limit handling...")
    try:
        client = WPEngineAPI()
        # Make multiple requests in quick succession
        for _ in range(100):
            client.sites.list()
    except RateLimitError as e:
        print(f"Rate limit error caught: {e}")
        if e.retry_after:
            print(f"Retry after: {e.retry_after} seconds")

def demonstrate_backup_error_handling():
    """Demonstrate error handling with backup operations."""
    print("\nDemonstrating backup error handling...")
    try:
        client = WPEngineAPI()
        # Try to create a backup for non-existent site
        backup_data = BackupCreate(
            description="Test backup",
            notification_emails=["test@example.com"]
        )
        client.backups.create("nonexistent_site_id", backup_data)
    except ResourceNotFoundError as e:
        print(f"Resource not found error caught: {e}")
    except ValidationError as e:
        print(f"Validation error caught: {e}")
    except WPEngineAPIError as e:
        print(f"General API error caught: {e}")

def demonstrate_network_error():
    """Demonstrate handling of network errors."""
    print("\nDemonstrating network error handling...")
    try:
        # Initialize client with invalid base URL
        client = WPEngineAPI(base_url="https://invalid-url.example.com")
        client.sites.list()
    except NetworkError as e:
        print(f"Network error caught: {e}")

def main():
    """Run all error handling demonstrations."""
    try:
        demonstrate_authentication_error()
        demonstrate_resource_not_found()
        demonstrate_validation_error()
        demonstrate_rate_limit_error()
        demonstrate_backup_error_handling()
        demonstrate_network_error()

    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

    print("\nAll error handling demonstrations completed!")

if __name__ == "__main__":
    main()
