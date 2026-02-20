#!/bin/bash

# Automatic GitHub Save Script

# Check if we're in a git repository
if [ ! -d .git ]; then
    echo "Not in a git repository. Initializing..."
    git init
fi

# Add all changes
git add .

# Commit with timestamp
git commit -m "Auto-save: $(date '+%Y-%m-%d %H:%M:%S')"

# Push to remote (assumes remote is set up)
git push origin main