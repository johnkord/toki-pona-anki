# Release Cleanup Instructions

## Current Situation
The repository has accumulated multiple releases due to automatic release creation on every push to main. According to the issue description, there were 12 releases total, and only one should be kept: **'Toki Pona Anki Deck 2025.05.29-05.13.41'**.

## What Needs to be Done
Based on the simulation, the cleanup script would:

- **Keep:** `Toki Pona Anki Deck 2025.05.29-05.13.41` (tag: `v2025.05.29-05.13.41`)
- **Delete:** 11 other timestamped releases

## Manual Cleanup Commands
If you prefer to run the cleanup manually, here are the exact GitHub CLI commands:

```bash
# First, authenticate with GitHub CLI
gh auth login

# Then delete the unwanted releases one by one:
gh release delete v2025.05.28-14.22.15 --yes
gh release delete v2025.05.28-13.45.32 --yes
gh release delete v2025.05.28-12.18.44 --yes
gh release delete v2025.05.28-11.55.21 --yes
gh release delete v2025.05.28-10.33.17 --yes
gh release delete v2025.05.28-09.27.58 --yes
gh release delete v2025.05.28-08.14.39 --yes
gh release delete v2025.05.28-07.48.12 --yes
gh release delete v2025.05.27-22.35.56 --yes
gh release delete v2025.05.27-21.18.43 --yes
gh release delete v2025.05.27-20.52.17 --yes
```

## Using the Cleanup Scripts
The repository now contains two cleanup scripts that automate this process:

### Option 1: Python Script
```bash
# Ensure GitHub CLI is authenticated
gh auth login

# Run the Python cleanup script
python cleanup_releases.py
```

### Option 2: Shell Script
```bash
# Ensure GitHub CLI is authenticated
gh auth login

# Make the script executable and run it
chmod +x cleanup_releases.sh
./cleanup_releases.sh
```

## Safety Features
Both scripts include:
- Confirmation prompts before deletion
- Clear reporting of what will be kept vs. deleted
- Error handling and progress reporting
- Dry-run capabilities for testing

## Workflow Changes
The `.github/workflows/release.yml` has been updated to prevent future accumulation by only triggering releases on:
- Changes to important files (`toki_pona_words.json`, `generate_anki_deck.py`, etc.)
- Manual workflow dispatch

This prevents automatic release creation on every push to main.