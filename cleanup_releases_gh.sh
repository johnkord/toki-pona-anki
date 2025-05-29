#!/bin/bash
set -e

# GitHub Release Cleanup Script
# Deletes all releases except 'Toki Pona Anki Deck 2025.05.29-05.13.41'

REPO="johnkord/toki-pona-anki"
KEEP_RELEASE="Toki Pona Anki Deck 2025.05.29-05.13.41"
KEEP_TAG="v2025.05.29-05.13.41"

echo "GitHub Release Cleanup Script"
echo "============================="
echo "Repository: $REPO"
echo "Keeping only: $KEEP_RELEASE"
echo "Tag: $KEEP_TAG"
echo

# Check for GitHub token
if [[ -z "$GITHUB_TOKEN" && -z "$RELEASE_GITHUB_TOKEN" && -z "$GH_TOKEN" ]]; then
    echo "❌ Error: No GitHub token found!"
    echo "Please set one of these environment variables:"
    echo "  export GITHUB_TOKEN=your_token_here"
    echo "  export RELEASE_GITHUB_TOKEN=your_token_here"
    echo "  export GH_TOKEN=your_token_here"
    echo
    echo "The token needs 'repo' permissions to delete releases."
    exit 1
fi

# Set GH_TOKEN for gh CLI
export GH_TOKEN="${GITHUB_TOKEN:-${RELEASE_GITHUB_TOKEN:-${GH_TOKEN}}}"

echo "✅ GitHub token configured"

# Test authentication
echo "Testing GitHub CLI authentication..."
if ! gh auth status >/dev/null 2>&1; then
    echo "❌ GitHub CLI authentication failed"
    echo "Token may be invalid or lack required permissions"
    exit 1
fi

echo "✅ GitHub CLI authenticated successfully"
echo

# Get releases
echo "Fetching releases from $REPO..."
RELEASES_JSON=$(gh api "repos/$REPO/releases" --method GET)

if [[ -z "$RELEASES_JSON" ]]; then
    echo "❌ Failed to fetch releases"
    exit 1
fi

echo "✅ Releases fetched successfully"

# Parse releases and find the one to keep
RELEASE_COUNT=$(echo "$RELEASES_JSON" | jq '. | length')
echo "Found $RELEASE_COUNT releases:"

KEEP_RELEASE_ID=""
RELEASES_TO_DELETE=()

while IFS= read -r release; do
    id=$(echo "$release" | jq -r '.id')
    name=$(echo "$release" | jq -r '.name')
    tag=$(echo "$release" | jq -r '.tag_name')
    
    echo "  - '$name' (tag: '$tag', id: $id)"
    
    if [[ "$name" == "$KEEP_RELEASE" || "$tag" == "$KEEP_TAG" ]]; then
        KEEP_RELEASE_ID="$id"
        echo "    ✅ This release will be KEPT"
    else
        RELEASES_TO_DELETE+=("$id:$name")
        echo "    🗑️  This release will be DELETED"
    fi
done < <(echo "$RELEASES_JSON" | jq -c '.[]')

echo

if [[ -z "$KEEP_RELEASE_ID" ]]; then
    echo "⚠️  Warning: Release to keep ('$KEEP_RELEASE') not found!"
    echo "Available releases:"
    echo "$RELEASES_JSON" | jq -r '.[] | "  - \(.name) (tag: \(.tag_name))"'
    echo
    echo "Proceeding with deletion of all found releases..."
fi

if [[ ${#RELEASES_TO_DELETE[@]} -eq 0 ]]; then
    echo "✅ No releases to delete - cleanup already complete!"
    exit 0
fi

echo "Planning to delete ${#RELEASES_TO_DELETE[@]} releases"
echo

# Delete releases
echo "🗑️  Starting release deletion..."
SUCCESS_COUNT=0
FAILED_COUNT=0

for item in "${RELEASES_TO_DELETE[@]}"; do
    release_id="${item%%:*}"
    release_name="${item#*:}"
    
    echo "Deleting: '$release_name' (id: $release_id)..."
    
    if gh api "repos/$REPO/releases/$release_id" --method DELETE >/dev/null 2>&1; then
        echo "  ✅ Successfully deleted '$release_name'"
        ((SUCCESS_COUNT++))
    else
        echo "  ❌ Failed to delete '$release_name'"
        ((FAILED_COUNT++))
    fi
done

echo
echo "Cleanup Summary:"
echo "==============="
echo "✅ Successfully deleted: $SUCCESS_COUNT releases"
if [[ $FAILED_COUNT -gt 0 ]]; then
    echo "❌ Failed to delete: $FAILED_COUNT releases"
fi
if [[ -n "$KEEP_RELEASE_ID" ]]; then
    echo "✅ Preserved release: '$KEEP_RELEASE'"
fi

if [[ $FAILED_COUNT -eq 0 && $SUCCESS_COUNT -gt 0 ]]; then
    echo
    echo "🎉 Release cleanup completed successfully!"
    echo "Only '$KEEP_RELEASE' remains."
elif [[ $SUCCESS_COUNT -eq 0 && $FAILED_COUNT -eq 0 ]]; then
    echo
    echo "✅ No action needed - cleanup was already complete."
else
    echo
    echo "⚠️  Partial success - $FAILED_COUNT releases could not be deleted."
    echo "Please check for permissions or network issues."
    exit 1
fi