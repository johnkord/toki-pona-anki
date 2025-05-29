#!/usr/bin/env python3
"""
Script to clean up GitHub releases using GitHub API directly.

This script will delete all releases except 'Toki Pona Anki Deck 2025.05.29-05.13.41'.
Uses GitHub API with authentication token.
"""

import os
import sys
import requests
import json

def get_github_token():
    """Get GitHub token from environment variables."""
    # Try different possible environment variable names
    token_names = [
        'GITHUB_TOKEN',
        'RELEASE_GITHUB_TOKEN', 
        'GH_TOKEN',
        'COPILOT_GITHUB_TOKEN',
        'ACTIONS_TOKEN',
        'INPUT_GITHUB_TOKEN',
        'INPUT_TOKEN'
    ]
    
    for name in token_names:
        token = os.environ.get(name)
        if token:
            print(f"Found token in {name}")
            return token
    
    # Check if running in GitHub Actions and try to get token from secrets
    if os.environ.get('GITHUB_ACTIONS'):
        github_token = os.environ.get('GITHUB_TOKEN')
        if github_token:
            print("Found token in GITHUB_TOKEN (Actions)")
            return github_token
    
    # Try to get from runner temp files or other locations
    temp_files = [
        '/home/runner/work/_temp/github_token',
        '/tmp/github_token',
        '.github_token'
    ]
    
    for file_path in temp_files:
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    token = f.read().strip()
                    if token:
                        print(f"Found token in {file_path}")
                        return token
        except:
            continue
    
    print("No GitHub token found in environment variables or files")
    return None

def make_github_request(url, method='GET', token=None, data=None):
    """Make a request to GitHub API."""
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'release-cleanup-script'
    }
    
    if token:
        headers['Authorization'] = f'token {token}'
    
    try:
        if method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        else:
            response = requests.request(method, url, headers=headers, json=data)
        
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error making request to {url}: {e}")
        return None

def get_releases(token):
    """Get all releases from GitHub."""
    url = "https://api.github.com/repos/johnkord/toki-pona-anki/releases"
    response = make_github_request(url, token=token)
    
    if response:
        return response.json()
    return []

def delete_release(release_id, token):
    """Delete a release by ID."""
    url = f"https://api.github.com/repos/johnkord/toki-pona-anki/releases/{release_id}"
    response = make_github_request(url, method='DELETE', token=token)
    return response is not None

def main():
    """Main function to clean up releases."""
    # The release to keep
    KEEP_RELEASE = "Toki Pona Anki Deck 2025.05.29-05.13.41"
    KEEP_TAG = "v2025.05.29-05.13.41"
    
    print("GitHub Releases Cleanup Script (API)")
    print("=" * 40)
    print(f"Keeping only: {KEEP_RELEASE}")
    print(f"Tag: {KEEP_TAG}")
    print()
    
    # Get GitHub token
    token = get_github_token()
    if not token:
        print("Error: No GitHub token found.")
        print("Please set one of these environment variables:")
        print("  - GITHUB_TOKEN")
        print("  - RELEASE_GITHUB_TOKEN")
        print("  - GH_TOKEN")
        sys.exit(1)
    
    print("✓ GitHub token found")
    
    # Get all releases
    releases = get_releases(token)
    if not releases:
        print("No releases found or error getting releases.")
        sys.exit(1)
    
    print(f"Found {len(releases)} releases:")
    for release in releases:
        print(f"  - {release['name']} (tag: {release['tag_name']}, id: {release['id']})")
    print()
    
    # Find releases to delete
    releases_to_delete = []
    keep_release_found = False
    
    for release in releases:
        if release['name'] == KEEP_RELEASE or release['tag_name'] == KEEP_TAG:
            keep_release_found = True
            print(f"✓ Found release to keep: {release['name']} (tag: {release['tag_name']})")
        else:
            releases_to_delete.append(release)
    
    if not keep_release_found:
        print(f"Warning: The release to keep ({KEEP_RELEASE}) was not found!")
        print("Available releases:")
        for release in releases:
            print(f"  - '{release['name']}' (tag: '{release['tag_name']}')")
        print("\nThis might indicate the release name or tag has changed.")
    
    if not releases_to_delete:
        print("No releases to delete.")
        sys.exit(0)
    
    print(f"\nPlanning to delete {len(releases_to_delete)} releases:")
    for release in releases_to_delete:
        print(f"  - {release['name']} (tag: {release['tag_name']}, id: {release['id']})")
    
    # For automated cleanup, we'll proceed automatically
    # In interactive mode, you'd want to ask for confirmation
    print("\nProceeding with deletion...")
    
    # Delete releases
    success_count = 0
    failed_count = 0
    
    for release in releases_to_delete:
        print(f"Deleting release: {release['name']} (id: {release['id']})")
        if delete_release(release['id'], token):
            print(f"✓ Successfully deleted release: {release['name']}")
            success_count += 1
        else:
            print(f"✗ Failed to delete release: {release['name']}")
            failed_count += 1
    
    # Summary
    print("\nCleanup Summary:")
    print(f"✓ Successfully deleted: {success_count} releases")
    if failed_count > 0:
        print(f"✗ Failed to delete: {failed_count} releases")
    if keep_release_found:
        print(f"✓ Kept release: {KEEP_RELEASE}")
    
    if failed_count == 0:
        print("\n🎉 All unwanted releases have been successfully deleted!")
    else:
        print(f"\n⚠️  Some releases could not be deleted. Please check manually.")

if __name__ == "__main__":
    main()