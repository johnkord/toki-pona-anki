#!/bin/bash
#
# Shell script to clean up GitHub releases, keeping only the specified release.
#
# This script will delete all releases except 'Toki Pona Anki Deck 2025.05.29-05.13.41'.
# Requires GitHub CLI (gh) to be installed and authenticated.
#

# The release to keep
KEEP_RELEASE="Toki Pona Anki Deck 2025.05.29-05.13.41"
KEEP_TAG="v2025.05.29-05.13.41"

echo "GitHub Releases Cleanup Script"
echo "==============================="
echo "Keeping only: $KEEP_RELEASE"
echo "Tag: $KEEP_TAG"
echo

# Check if gh CLI is available and authenticated
if ! command -v gh &> /dev/null; then
    echo "Error: GitHub CLI (gh) is not installed."
    echo "Please install it from: https://cli.github.com/"
    exit 1
fi

if ! gh auth status &> /dev/null; then
    echo "Error: GitHub CLI is not authenticated."
    echo "Please run: gh auth login"
    exit 1
fi

# Get all releases
echo "Fetching releases..."
releases=$(gh release list --json name,tagName)

if [ $? -ne 0 ] || [ -z "$releases" ]; then
    echo "Error: Could not fetch releases."
    exit 1
fi

echo "Current releases:"
echo "$releases" | jq -r '.[] | "  - \(.name) (tag: \(.tagName))"'
echo

# Find releases to delete (all except the one to keep)
releases_to_delete=$(echo "$releases" | jq -r --arg keep_release "$KEEP_RELEASE" --arg keep_tag "$KEEP_TAG" '.[] | select(.name != $keep_release and .tagName != $keep_tag) | .tagName')

# Check if the release to keep exists
keep_release_found=$(echo "$releases" | jq -r --arg keep_release "$KEEP_RELEASE" --arg keep_tag "$KEEP_TAG" '.[] | select(.name == $keep_release or .tagName == $keep_tag) | .tagName')

if [ -z "$keep_release_found" ]; then
    echo "Warning: The release to keep ($KEEP_RELEASE) was not found!"
    echo "This might indicate the release name or tag has changed."
    read -p "Do you want to continue with deletion anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Aborted."
        exit 1
    fi
else
    echo "✓ Found release to keep: $KEEP_RELEASE (tag: $keep_release_found)"
fi

if [ -z "$releases_to_delete" ]; then
    echo "No releases to delete."
    exit 0
fi

echo
echo "Planning to delete the following releases:"
for tag in $releases_to_delete; do
    release_name=$(echo "$releases" | jq -r --arg tag "$tag" '.[] | select(.tagName == $tag) | .name')
    echo "  - $release_name (tag: $tag)"
done

echo
read -p "Are you sure you want to delete these releases? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Aborted."
    exit 0
fi

# Delete releases
echo
echo "Deleting releases..."
success_count=0
failed_count=0

for tag in $releases_to_delete; do
    release_name=$(echo "$releases" | jq -r --arg tag "$tag" '.[] | select(.tagName == $tag) | .name')
    echo "Deleting release: $release_name (tag: $tag)"
    
    if gh release delete "$tag" --yes; then
        echo "✓ Successfully deleted release: $tag"
        ((success_count++))
    else
        echo "✗ Failed to delete release: $tag"
        ((failed_count++))
    fi
done

# Summary
echo
echo "Cleanup Summary:"
echo "✓ Successfully deleted: $success_count releases"
if [ $failed_count -gt 0 ]; then
    echo "✗ Failed to delete: $failed_count releases"
fi
echo "✓ Kept release: $KEEP_RELEASE"

if [ $failed_count -eq 0 ]; then
    echo
    echo "🎉 All unwanted releases have been successfully deleted!"
else
    echo
    echo "⚠️  Some releases could not be deleted. Please check manually."
fi