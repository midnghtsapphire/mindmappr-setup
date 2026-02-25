#!/bin/bash

# Ensure SSH directory exists
mkdir -p ~/.ssh
chmod 700 ~/.ssh

# Generate ED25519 SSH Key
ssh-keygen -t ed25519 -C "claw@openclaw-midnghtsapphire" -f ~/.ssh/id_midnghtsapphire -N ""

# Set proper permissions
chmod 600 ~/.ssh/id_midnghtsapphire
chmod 644 ~/.ssh/id_midnghtsapphire.pub

# Display public key for GitHub
cat ~/.ssh/id_midnghtsapphire.pub

# Configure Git
git config --global user.name "Claw (OpenClaw)"
git config --global user.email "claw@openclaw-midnghtsapphire"

# Create GitHub access script
cat > ~/.ssh/github_access.sh << EOL
#!/bin/bash
# GitHub Repository Cloning Script

# List of repositories to clone
REPOS=(
    "git@github.com:MIDNGHTSAPPHIRE/Universal-OZ.git"
    "git@github.com:MIDNGHTSAPPHIRE/SSRN-AUTOMATION.git"
    "git@github.com:MIDNGHTSAPPHIRE/the-alt-text.git"
    "git@github.com:MIDNGHTSAPPHIRE/Neurooz.git"
)

# Clone repositories
for repo in "${REPOS[@]}"; do
    git clone $repo
done
EOL

chmod +x ~/.ssh/github_access.sh

echo "GitHub setup complete. Please add the SSH public key to your GitHub account."