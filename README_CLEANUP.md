# Release Cleanup Instructions

This document provides instructions for cleaning up GitHub releases, keeping only 'Toki Pona Anki Deck 2025.05.29-05.13.41'.

## Problem
The repository has multiple releases due to automatic creation on every push. We need to clean up all releases except the specified one.

## Solutions Available

### 1. Automated Workflow (Recommended)
A GitHub Actions workflow has been created that can be manually triggered:

```bash
# Go to the Actions tab in GitHub
# Find "Cleanup Releases" workflow
# Click "Run workflow"
```

The workflow file is: `.github/workflows/cleanup-releases.yml`

### 2. Manual Execution with GitHub CLI

If you have GitHub CLI installed and authenticated:

```bash
# Make sure you're authenticated
gh auth login

# Run the cleanup script
./cleanup_releases_gh.sh
```

### 3. Manual Execution with Python

If you prefer Python:

```bash
# Set your GitHub token
export GITHUB_TOKEN="your_token_here"
# or
export RELEASE_GITHUB_TOKEN="your_token_here"

# Run the Python script
python cleanup_releases_final.py
```

### 4. Manual GitHub CLI Commands

If you want to run commands manually:

```bash
# List all releases
gh api repos/johnkord/toki-pona-anki/releases

# Delete specific releases (replace ID with actual release ID)
gh api repos/johnkord/toki-pona-anki/releases/RELEASE_ID --method DELETE
```

## Authentication Requirements

All methods require a GitHub token with `repo` permissions. The token should be:
- Set as `GITHUB_TOKEN`, `RELEASE_GITHUB_TOKEN`, or `GH_TOKEN` environment variable
- The same token used in the release workflow (`secrets.RELEASE_GITHUB_TOKEN`)

## What Will Be Kept

Only this release will be preserved:
- **Name**: Toki Pona Anki Deck 2025.05.29-05.13.41
- **Tag**: v2025.05.29-05.13.41

All other releases will be deleted.

## Safety Features

- Scripts identify which release will be kept before deletion
- Clear reporting of what will be deleted vs. preserved
- Error handling and detailed status reporting
- Confirmation of successful deletions

## Troubleshooting

If you encounter authentication issues:
1. Verify your token has `repo` permissions
2. Check that the token is not expired
3. Ensure you're using the correct token environment variable name

If the target release is not found:
- Check the exact name and tag in the GitHub releases page
- The scripts will warn you and show available releases
- You can proceed with caution or update the target release name in the scripts