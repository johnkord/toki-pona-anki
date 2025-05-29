#!/usr/bin/env python3
"""
Script to clean up GitHub releases, keeping only the specified release.

This script will delete all releases except 'Toki Pona Anki Deck 2025.05.29-05.13.41'.
Requires GitHub CLI (gh) to be installed and authenticated.
"""

import subprocess
import sys
import json

def run_command(cmd):
    """Run a command and return its output."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}")
        print(f"Error: {e.stderr}")
        return None

def get_releases():
    """Get all releases from GitHub."""
    output = run_command("gh release list --json name,tagName")
    if output:
        return json.loads(output)
    return []

def delete_release(tag_name):
    """Delete a release by tag name."""
    print(f"Deleting release: {tag_name}")
    result = run_command(f"gh release delete {tag_name} --yes")
    if result is not None:
        print(f"✓ Successfully deleted release: {tag_name}")
        return True
    else:
        print(f"✗ Failed to delete release: {tag_name}")
        return False

def main():
    """Main function to clean up releases."""
    # The release to keep
    KEEP_RELEASE = "Toki Pona Anki Deck 2025.05.29-05.13.41"
    KEEP_TAG = "v2025.05.29-05.13.41"
    
    print("GitHub Releases Cleanup Script")
    print("=" * 40)
    print(f"Keeping only: {KEEP_RELEASE}")
    print(f"Tag: {KEEP_TAG}")
    print()
    
    # Check if gh CLI is available and authenticated
    auth_status = run_command("gh auth status")
    if auth_status is None:
        print("Error: GitHub CLI is not authenticated.")
        print("Please run: gh auth login")
        sys.exit(1)
    
    # Get all releases
    releases = get_releases()
    if not releases:
        print("No releases found or error getting releases.")
        sys.exit(1)
    
    print(f"Found {len(releases)} releases:")
    for release in releases:
        print(f"  - {release['name']} (tag: {release['tagName']})")
    print()
    
    # Find releases to delete
    releases_to_delete = []
    keep_release_found = False
    
    for release in releases:
        if release['name'] == KEEP_RELEASE or release['tagName'] == KEEP_TAG:
            keep_release_found = True
            print(f"✓ Found release to keep: {release['name']} (tag: {release['tagName']})")
        else:
            releases_to_delete.append(release)
    
    if not keep_release_found:
        print(f"Warning: The release to keep ({KEEP_RELEASE}) was not found!")
        print("This might indicate the release name or tag has changed.")
        response = input("Do you want to continue with deletion anyway? (y/N): ")
        if response.lower() != 'y':
            print("Aborted.")
            sys.exit(1)
    
    if not releases_to_delete:
        print("No releases to delete.")
        sys.exit(0)
    
    print(f"\nPlanning to delete {len(releases_to_delete)} releases:")
    for release in releases_to_delete:
        print(f"  - {release['name']} (tag: {release['tagName']})")
    
    # Confirm deletion
    print()
    response = input("Are you sure you want to delete these releases? (y/N): ")
    if response.lower() != 'y':
        print("Aborted.")
        sys.exit(0)
    
    # Delete releases
    print("\nDeleting releases...")
    success_count = 0
    failed_count = 0
    
    for release in releases_to_delete:
        if delete_release(release['tagName']):
            success_count += 1
        else:
            failed_count += 1
    
    # Summary
    print("\nCleanup Summary:")
    print(f"✓ Successfully deleted: {success_count} releases")
    if failed_count > 0:
        print(f"✗ Failed to delete: {failed_count} releases")
    print(f"✓ Kept release: {KEEP_RELEASE}")
    
    if failed_count == 0:
        print("\n🎉 All unwanted releases have been successfully deleted!")
    else:
        print(f"\n⚠️  Some releases could not be deleted. Please check manually.")

if __name__ == "__main__":
    main()