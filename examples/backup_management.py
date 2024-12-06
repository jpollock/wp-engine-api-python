"""Backup management example for the WP Engine API Python SDK."""

import time
from wp_engine_api import WPEngineAPI
from wp_engine_api.models import BackupCreate, BackupStatus

def wait_for_backup(client, site_id: str, backup_id: str, timeout: int = 300) -> None:
    """Wait for backup to complete.

    Args:
        client: WPEngineAPI instance
        site_id: Site ID
        backup_id: Backup ID
        timeout: Maximum time to wait in seconds
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        backup = client.backups.get(site_id, backup_id)
        print(f"Backup status: {backup.status}")
        
        if backup.status == BackupStatus.COMPLETE:
            print("Backup completed successfully!")
            return
        elif backup.status == BackupStatus.FAILED:
            print("Backup failed!")
            return
        
        time.sleep(10)  # Wait 10 seconds before checking again
    
    print("Timeout waiting for backup to complete")

def main():
    # Initialize client
    client = WPEngineAPI()

    try:
        # List all sites
        sites = client.sites.list()
        if not sites:
            print("No sites found")
            return

        # Use the first site for this example
        site = sites[0]
        print(f"\nWorking with site: {site.name} (ID: {site.id})")

        # List existing backups
        print("\nExisting backups:")
        backups = client.backups.list(site.id)
        for backup in backups:
            print(f"- {backup.created_at}: {backup.description or 'No description'}")
            print(f"  Status: {backup.status}")
            print(f"  Size: {backup.size if backup.size else 'Unknown'}")
            if backup.download_url:
                print(f"  Download URL: {backup.download_url}")
            print()

        # Create a new backup
        print("\nCreating new backup...")
        backup_data = BackupCreate(
            description="Example backup from Python SDK",
            notification_emails=["admin@example.com"]
        )
        
        new_backup = client.backups.create(site.id, backup_data)
        print(f"Backup created with ID: {new_backup.id}")

        # Wait for backup to complete
        print("\nWaiting for backup to complete...")
        wait_for_backup(client, site.id, new_backup.id)

        # Get final backup details
        final_backup = client.backups.get(site.id, new_backup.id)
        print("\nFinal backup details:")
        print(f"Status: {final_backup.status}")
        print(f"Created at: {final_backup.created_at}")
        if final_backup.completed_at:
            print(f"Completed at: {final_backup.completed_at}")
        if final_backup.size:
            print(f"Size: {final_backup.size} bytes")
        if final_backup.download_url:
            print(f"Download URL: {final_backup.download_url}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
