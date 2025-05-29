#!/usr/bin/env python3
"""
Simulation script to show what the cleanup would do without GitHub CLI authentication.
This simulates the cleanup process using mock data to demonstrate functionality.
"""

import subprocess
import json

def try_get_actual_releases():
    """Try to get actual releases if GitHub CLI is available and authenticated."""
    try:
        result = subprocess.run(
            ["gh", "release", "list", "--json", "name,tagName"], 
            capture_output=True, text=True, check=True
        )
        return json.loads(result.stdout)
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
        return None

def simulate_releases():
    """Simulate the releases that would typically exist based on the problem description."""
    # Based on the problem statement, there were 12 releases with timestamps
    # Only one should be kept: 'Toki Pona Anki Deck 2025.05.29-05.13.41'
    mock_releases = [
        {'name': 'Toki Pona Anki Deck 2025.05.29-05.13.41', 'tagName': 'v2025.05.29-05.13.41'},
        {'name': 'Toki Pona Anki Deck 2025.05.28-14.22.15', 'tagName': 'v2025.05.28-14.22.15'},
        {'name': 'Toki Pona Anki Deck 2025.05.28-13.45.32', 'tagName': 'v2025.05.28-13.45.32'},
        {'name': 'Toki Pona Anki Deck 2025.05.28-12.18.44', 'tagName': 'v2025.05.28-12.18.44'},
        {'name': 'Toki Pona Anki Deck 2025.05.28-11.55.21', 'tagName': 'v2025.05.28-11.55.21'},
        {'name': 'Toki Pona Anki Deck 2025.05.28-10.33.17', 'tagName': 'v2025.05.28-10.33.17'},
        {'name': 'Toki Pona Anki Deck 2025.05.28-09.27.58', 'tagName': 'v2025.05.28-09.27.58'},
        {'name': 'Toki Pona Anki Deck 2025.05.28-08.14.39', 'tagName': 'v2025.05.28-08.14.39'},
        {'name': 'Toki Pona Anki Deck 2025.05.28-07.48.12', 'tagName': 'v2025.05.28-07.48.12'},
        {'name': 'Toki Pona Anki Deck 2025.05.27-22.35.56', 'tagName': 'v2025.05.27-22.35.56'},
        {'name': 'Toki Pona Anki Deck 2025.05.27-21.18.43', 'tagName': 'v2025.05.27-21.18.43'},
        {'name': 'Toki Pona Anki Deck 2025.05.27-20.52.17', 'tagName': 'v2025.05.27-20.52.17'},
    ]
    return mock_releases

def main():
    """Simulate the cleanup process."""
    KEEP_RELEASE = "Toki Pona Anki Deck 2025.05.29-05.13.41"
    KEEP_TAG = "v2025.05.29-05.13.41"
    
    print("SIMULATION: GitHub Releases Cleanup Script")
    print("=" * 50)
    print(f"This is a simulation showing what would happen")
    print(f"Keeping only: {KEEP_RELEASE}")
    print(f"Tag: {KEEP_TAG}")
    print()
    
    # Try to get actual releases first, fall back to simulation
    releases = try_get_actual_releases()
    if releases:
        print("Using actual release data from GitHub")
    else:
        print("GitHub CLI not available or not authenticated - using simulated data")
        releases = simulate_releases()
    
    print(f"SIMULATION: Found {len(releases)} releases:")
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
    
    print(f"\nSIMULATION: Would delete {len(releases_to_delete)} releases:")
    for release in releases_to_delete:
        print(f"  - {release['name']} (tag: {release['tagName']})")
    
    print(f"\nSIMULATION: Commands that would be executed:")
    for release in releases_to_delete:
        print(f"  gh release delete {release['tagName']} --yes")
    
    print(f"\nSIMULATION Summary:")
    print(f"✓ Would delete: {len(releases_to_delete)} releases")
    print(f"✓ Would keep: {KEEP_RELEASE}")
    print()
    print("To actually run the cleanup:")
    print("1. Ensure GitHub CLI is installed and authenticated: gh auth login")
    print("2. Run: python cleanup_releases.py")
    print("3. Or run: ./cleanup_releases.sh")

if __name__ == "__main__":
    main()