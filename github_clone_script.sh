#!/bin/bash

# GitHub Repository Cloning Script for MIDNGHTSAPPHIRE

# Ensure workspace directory exists
mkdir -p ~/github/MIDNGHTSAPPHIRE

# Change to workspace directory
cd ~/github/MIDNGHTSAPPHIRE

# List of repositories to clone (placeholder for key repositories)
REPOS=(
    "https://github.com/MIDNGHTSAPPHIRE/Universal-OZ.git"
    "https://github.com/MIDNGHTSAPPHIRE/SSRN-AUTOMATION.git"
    "https://github.com/MIDNGHTSAPPHIRE/the-alt-text.git"
    "https://github.com/MIDNGHTSAPPHIRE/Neurooz.git"
)

# Clone repositories
for repo in "${REPOS[@]}"; do
    git clone $repo
done

# List cloned repositories
ls -l