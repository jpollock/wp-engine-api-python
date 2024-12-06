"""Basic usage example for the WP Engine API Python SDK."""

import os
from wp_engine_api import WPEngineAPI

def main():
    """Demonstrate basic usage of the SDK."""
    # Method 1: Initialize with username and password directly
    client1 = WPEngineAPI(
        username="your-username",
        password="your-password"
    )

    # Method 2: Initialize using environment variables
    # Requires setting:
    # - WP_ENGINE_API_USERNAME
    # - WP_ENGINE_API_PASSWORD
    # Either in the environment or in a .env file
    client2 = WPEngineAPI()

    # Use whichever client is properly configured
    client = client1 if os.getenv("WP_ENGINE_API_USERNAME") is None else client2

    try:
        # List all sites
        print("\nListing your sites:")
        sites = client.sites.list()
        for site in sites:
            print(f"- {site.name} (ID: {site.id})")
            print(f"  Environment: {site.environment}")
            print(f"  Status: {site.status}")
            print(f"  Created: {site.created_at}")
            if site.domain:
                print(f"  Domain: {site.domain}")
            print()

        # Get current user
        print("\nGetting current user details:")
        user = client.users.get_current()
        print(f"Email: {user.email}")
        print(f"Name: {user.first_name} {user.last_name}")

        # Get a specific site
        if sites:
            site_id = sites[0].id
            print(f"\nGetting detailed information for site {site_id}:")
            site = client.sites.get(site_id)
            print(f"Name: {site.name}")
            print(f"PHP Version: {site.php_version}")
            print(f"WordPress Version: {site.wordpress_version}")
            print(f"Environment: {site.environment}")
            print(f"Status: {site.status}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()
