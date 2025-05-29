#!/usr/bin/env python3
"""
Release cleanup script that can be executed with proper GitHub authentication.

This script will delete all releases except 'Toki Pona Anki Deck 2025.05.29-05.13.41'.
It requires GITHUB_TOKEN or RELEASE_GITHUB_TOKEN to be set in the environment.
"""

import os
import sys
import subprocess
import json

def run_gh_command(cmd):
    """Run a gh CLI command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {cmd}")
        print(f"Error: {e.stderr}")
        return None

def main():
    """Main function to clean up releases."""
    # The release to keep
    KEEP_RELEASE = "Toki Pona Anki Deck 2025.05.29-05.13.41"
    KEEP_TAG = "v2025.05.29-05.13.41"
    
    print("GitHub Releases Cleanup Script")
    print("=" * 50)
    print(f"Repository: johnkord/toki-pona-anki")
    print(f"Keeping only: {KEEP_RELEASE}")
    print(f"Tag: {KEEP_TAG}")
    print()
    
    # Set up authentication
    github_token = (os.environ.get('GITHUB_TOKEN') or 
                   os.environ.get('RELEASE_GITHUB_TOKEN') or 
                   os.environ.get('GH_TOKEN'))
    
    if github_token:
        os.environ['GH_TOKEN'] = github_token
        print("✓ GitHub token found and configured")
    else:
        print("✗ No GitHub token found in environment variables:")
        print("  - GITHUB_TOKEN")
        print("  - RELEASE_GITHUB_TOKEN") 
        print("  - GH_TOKEN")
        print()
        print("Please set one of these environment variables with a GitHub token")
        print("that has 'repo' permissions.")
        return 1
    
    # Test authentication
    auth_test = run_gh_command("gh auth status")
    if auth_test is None:
        print("✗ GitHub CLI authentication failed")
        print("Please ensure your token has the correct permissions")
        return 1
    
    print("✓ GitHub CLI authenticated successfully")
    print()
    
    # Get all releases
    print("Fetching releases...")
    releases_output = run_gh_command("gh api repos/johnkord/toki-pona-anki/releases --method GET")
    
    if releases_output is None:
        print("✗ Failed to fetch releases")
        return 1
    
    try:
        releases = json.loads(releases_output)
    except json.JSONDecodeError:
        print("✗ Failed to parse releases JSON")
        return 1
    
    print(f"Found {len(releases)} releases:")
    for release in releases:
        print(f"  - '{release['name']}' (tag: '{release['tag_name']}', id: {release['id']})")
    print()
    
    # Find releases to delete
    releases_to_delete = []
    keep_release_found = False
    
    for release in releases:
        if release['name'] == KEEP_RELEASE or release['tag_name'] == KEEP_TAG:
            keep_release_found = True
            print(f"✓ Found release to keep: '{release['name']}' (tag: '{release['tag_name']}')")
        else:
            releases_to_delete.append(release)
    
    if not keep_release_found:
        print(f"⚠️  Warning: The release to keep ('{KEEP_RELEASE}') was not found!")
        print("Available releases:")
        for release in releases:
            print(f"  - '{release['name']}' (tag: '{release['tag_name']}')")
        print()
        print("The script will proceed to delete all found releases.")
        print("Make sure this is what you want!")
    
    if not releases_to_delete:
        print("✓ No releases to delete - cleanup already complete!")
        return 0
    
    print(f"Planning to delete {len(releases_to_delete)} releases:")
    for release in releases_to_delete:
        print(f"  - '{release['name']}' (tag: '{release['tag_name']}', id: {release['id']})")
    print()
    
    # Perform deletion
    print("Proceeding with release deletion...")
    success_count = 0
    failed_count = 0
    
    for release in releases_to_delete:
        print(f"Deleting: '{release['name']}' (id: {release['id']})...")
        delete_cmd = f"gh api repos/johnkord/toki-pona-anki/releases/{release['id']} --method DELETE"
        
        if run_gh_command(delete_cmd) is not None:
            print(f"  ✓ Successfully deleted '{release['name']}'")
            success_count += 1
        else:
            print(f"  ✗ Failed to delete '{release['name']}'")
            failed_count += 1
    
    # Summary
    print()
    print("Cleanup Summary:")
    print("=" * 30)
    print(f"✓ Successfully deleted: {success_count} releases")
    if failed_count > 0:
        print(f"✗ Failed to delete: {failed_count} releases")
    if keep_release_found:
        print(f"✓ Preserved release: '{KEEP_RELEASE}'")
    
    if failed_count == 0 and success_count > 0:
        print("\n🎉 Release cleanup completed successfully!")
        print(f"Only '{KEEP_RELEASE}' remains.")
    elif success_count == 0 and failed_count == 0:
        print("\n✓ No action needed - cleanup was already complete.")
    else:
        print(f"\n⚠️  Partial success - {failed_count} releases could not be deleted.")
        print("Please check the error messages above and try again.")
    
    return 0 if failed_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())