# Release Management

This document describes how to manage releases for the Toki Pona Anki repository.

## Current Issue

The repository was automatically creating releases on every push to the main branch, which resulted in many releases being created. The goal is to keep only the release `Toki Pona Anki Deck 2025.05.29-05.13.41` and delete all others.

## Solution

### 1. Cleanup Existing Releases

Two scripts are provided to clean up existing releases:

#### Python Script (cleanup_releases.py)
```bash
python cleanup_releases.py
```

#### Shell Script (cleanup_releases.sh)
```bash
./cleanup_releases.sh
```

Both scripts will:
- List all current releases
- Identify the release to keep: `Toki Pona Anki Deck 2025.05.29-05.13.41` (tag: `v2025.05.29-05.13.41`)
- Delete all other releases
- Provide a summary of the cleanup operation

**Prerequisites:**
- GitHub CLI (`gh`) must be installed
- You must be authenticated with GitHub CLI (`gh auth login`)
- You must have appropriate permissions to delete releases

### 2. Prevent Future Release Accumulation

The GitHub Actions workflow has been modified to only create releases when:
- Changes are made to important files (`toki_pona_words.json`, `generate_anki_deck.py`, `generate_images.py`, `requirements.txt`)
- The workflow is manually triggered

This prevents automatic release creation on every push to main.

## Usage Instructions

1. **To clean up existing releases:**
   ```bash
   # Ensure you're authenticated with GitHub CLI
   gh auth login
   
   # Run the cleanup script (choose one)
   python cleanup_releases.py
   # OR
   ./cleanup_releases.sh
   ```

2. **To create a new release manually:**
   - Go to the GitHub repository
   - Click on "Actions" tab
   - Find the "Build and Release Anki Deck" workflow
   - Click "Run workflow" to trigger it manually

## What Each Script Does

### cleanup_releases.py
- Fetches all releases using GitHub CLI
- Identifies the release to keep based on name and tag
- Shows what will be deleted and asks for confirmation
- Deletes unwanted releases one by one
- Provides a detailed summary

### cleanup_releases.sh
- Similar functionality to the Python script
- Uses shell commands and `jq` for JSON processing
- More lightweight but requires `jq` to be installed

## Safety Features

Both scripts include safety features:
- List all releases before deletion
- Confirm the release to keep exists
- Ask for user confirmation before deletion
- Provide detailed feedback during the process
- Report success/failure for each operation

## Future Releases

After the cleanup, the workflow will only create new releases when:
1. You manually trigger the workflow from GitHub Actions
2. You push changes to files that affect the Anki deck generation

This ensures releases are only created when actually needed.