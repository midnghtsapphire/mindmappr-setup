#!/bin/bash
# Automatic GitHub Save Script - Updated 2026-02-25
# Saves workspace files to GitHub via SSH key authentication
# 
# Usage: ./save_to_github.sh [commit message]
# 
# The git repo is at /home/openclaw/.openclaw/workspace
# GitHub repo: https://github.com/midnghtsapphire/mindmappr-setup
# Files are tracked under workspace/ prefix in the repo

WORKSPACE_DIR="/home/openclaw/.openclaw/workspace"
SSH_KEY="/home/openclaw/.ssh/id_ed25519"
COMMIT_MSG="${1:-Auto-save: $(date '+%Y-%m-%d %H:%M:%S')}"

cd "$WORKSPACE_DIR"

# Check if we are in a git repository
if [ ! -d .git ]; then
    echo "ERROR: Not in a git repository. Run git init and set remote first."
    exit 1
fi

# Check remote is set
if ! git remote get-url origin &>/dev/null; then
    echo "Setting up remote..."
    git remote add origin git@github.com:midnghtsapphire/mindmappr-setup.git
fi

# Copy root-level files to workspace/ subdir for tracking
echo "Syncing files to workspace/ tracking directory..."
for f in *.py *.sh *.md *.json *.yml *.yaml *.toml; do
    [ -f "$f" ] && cp "$f" "workspace/$f" 2>/dev/null
done
# Sync subdirectories
for d in revvel-email-organizer revvel_email_organizer memory; do
    [ -d "$d" ] && cp -r "$d" "workspace/" 2>/dev/null
done

# Stage all changes in workspace/
git add workspace/

# Check if there is anything to commit
if git diff --cached --quiet; then
    echo "Nothing to commit."
    exit 0
fi

# Commit
git commit -m "$COMMIT_MSG"

# Push using SSH key
GIT_SSH_COMMAND="ssh -i $SSH_KEY -o StrictHostKeyChecking=no" git push origin main

echo "Done! Pushed to GitHub."
