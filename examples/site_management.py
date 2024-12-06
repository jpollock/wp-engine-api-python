"""Site management example for the WP Engine API Python SDK."""

from wp_engine_api import WPEngineAPI
from wp_engine_api.models import Environment, SiteCreate, SiteUpdate

def main():
    # Initialize client
    client = WPEngineAPI()

    try:
        # Create a new site
        print("\nCreating new site...")
        new_site_data = SiteCreate(
            name="Example Site",
            environment=Environment.DEVELOPMENT,
            php_version="8.1",
            wordpress_version="6.3"
        )
        
        new_site = client.sites.create(new_site_data)
        print(f"Site created successfully!")
        print(f"Site ID: {new_site.id}")
        print(f"Name: {new_site.name}")
        print(f"Environment: {new_site.environment}")
        print(f"PHP Version: {new_site.php_version}")
        print(f"WordPress Version: {new_site.wordpress_version}")

        # Update the site
        print("\nUpdating site...")
        update_data = SiteUpdate(
            name="Updated Example Site",
            php_version="8.2"
        )
        
        updated_site = client.sites.update(new_site.id, update_data)
        print("Site updated successfully!")
        print(f"New name: {updated_site.name}")
        print(f"New PHP version: {updated_site.php_version}")

        # List all sites
        print("\nListing all sites:")
        sites = client.sites.list()
        for site in sites:
            print(f"\n- {site.name} (ID: {site.id})")
            print(f"  Environment: {site.environment}")
            print(f"  Status: {site.status}")
            print(f"  Created: {site.created_at}")
            if site.domain:
                print(f"  Domain: {site.domain}")
            print(f"  PHP Version: {site.php_version}")
            print(f"  WordPress Version: {site.wordpress_version}")

        # Get detailed information about a specific site
        print(f"\nGetting detailed information for site {new_site.id}...")
        site_detail = client.sites.get(new_site.id)
        print("\nDetailed site information:")
        print(f"Name: {site_detail.name}")
        print(f"Environment: {site_detail.environment}")
        print(f"Status: {site_detail.status}")
        print(f"Created at: {site_detail.created_at}")
        print(f"Updated at: {site_detail.updated_at}")
        print(f"PHP Version: {site_detail.php_version}")
        print(f"WordPress Version: {site_detail.wordpress_version}")
        if site_detail.domain:
            print(f"Domain: {site_detail.domain}")

        # Delete the site (commented out for safety)
        # print(f"\nDeleting site {new_site.id}...")
        # client.sites.delete(new_site.id)
        # print("Site deleted successfully!")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
