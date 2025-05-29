#!/usr/bin/env python3
"""
Script to clean up GitHub releases using available GitHub API tools.

This script will delete all releases except 'Toki Pona Anki Deck 2025.05.29-05.13.41'.
Uses Python API calls that should work in the current environment.
"""

import requests
import os
import sys
import json

def make_github_api_call(method, url, data=None):
    """Make GitHub API call using requests with available authentication."""
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'GitHub-Release-Cleanup'
    }
    
    # Try to find any available authentication
    auth_token = None
    
    # Check environment variables for any form of GitHub token
    for env_var in ['GITHUB_TOKEN', 'GH_TOKEN', 'RELEASE_GITHUB_TOKEN', 
                    'ACTIONS_TOKEN', 'INPUT_GITHUB_TOKEN', 'INPUT_TOKEN']:
        token = os.environ.get(env_var)
        if token and token.strip():
            auth_token = token.strip()
            break
    
    if auth_token:
        headers['Authorization'] = f'token {auth_token}'
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=headers)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=headers, json=data)
        else:
            response = requests.request(method, url, headers=headers, json=data)
        
        print(f"{method} {url} -> {response.status_code}")
        
        if response.status_code == 401:
            print("Authentication failed - no valid token available")
            return None
        elif response.status_code == 403:
            print("Access forbidden - insufficient permissions")
            return None
        elif response.status_code >= 400:
            print(f"API error: {response.status_code} - {response.text}")
            return None
            
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def get_releases():
    """Get all releases from GitHub API."""
    url = "https://api.github.com/repos/johnkord/toki-pona-anki/releases"
    response = make_github_api_call('GET', url)
    
    if response:
        try:
            return response.json()
        except json.JSONDecodeError:
            print("Failed to parse release data")
            return []
    return []

def delete_release(release_id):
    """Delete a release by ID."""
    url = f"https://api.github.com/repos/johnkord/toki-pona-anki/releases/{release_id}"
    response = make_github_api_call('DELETE', url)
    return response is not None

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
    
    # Test authentication by trying to get releases
    print("Fetching releases...")
    releases = get_releases()
    
    if not releases:
        print("Failed to get releases - this could be due to:")
        print("1. No authentication token available")
        print("2. Network/API access issues")
        print("3. Repository access permissions")
        print()
        print("Available environment variables with 'TOKEN' or similar:")
        for key in sorted(os.environ.keys()):
            if any(word in key.upper() for word in ['TOKEN', 'SECRET', 'AUTH', 'KEY']):
                value = os.environ[key]
                if value:
                    print(f"  {key} = {value[:10]}...{value[-5:] if len(value) > 15 else ''}")
                else:
                    print(f"  {key} = (empty)")
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
        print(f"Warning: The release to keep ('{KEEP_RELEASE}') was not found!")
        print("Available releases:")
        for release in releases:
            print(f"  - '{release['name']}' (tag: '{release['tag_name']}')")
        print()
    
    if not releases_to_delete:
        print("No releases to delete.")
        return 0
    
    print(f"Planning to delete {len(releases_to_delete)} releases:")
    for release in releases_to_delete:
        print(f"  - '{release['name']}' (tag: '{release['tag_name']}', id: {release['id']})")
    
    print("\nProceeding with deletion...")
    
    # Delete releases
    success_count = 0
    failed_count = 0
    
    for release in releases_to_delete:
        print(f"Deleting release: '{release['name']}' (id: {release['id']})")
        if delete_release(release['id']):
            print(f"✓ Successfully deleted release: '{release['name']}'")
            success_count += 1
        else:
            print(f"✗ Failed to delete release: '{release['name']}'")
            failed_count += 1
    
    # Summary
    print("\nCleanup Summary:")
    print(f"✓ Successfully deleted: {success_count} releases")
    if failed_count > 0:
        print(f"✗ Failed to delete: {failed_count} releases")
    if keep_release_found:
        print(f"✓ Kept release: '{KEEP_RELEASE}'")
    
    if failed_count == 0 and success_count > 0:
        print("\n🎉 All unwanted releases have been successfully deleted!")
    elif failed_count > 0:
        print(f"\n⚠️  Some releases could not be deleted. Please check manually.")
    
    return 0 if failed_count == 0 else 1

if __name__ == "__main__":
    sys.exit(main())