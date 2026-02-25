#!/bin/bash

# Autonomous GitHub Access Setup

# Ensure SSH directory exists with secure permissions
mkdir -p ~/github_access
chmod 700 ~/github_access

# Generate ED25519 SSH Key with maximum security
ssh-keygen -t ed25519 \
    -f ~/github_access/id_midnghtsapphire \
    -C "claw@openclaw-midnghtsapphire" \
    -N ""

# Set strict permissions
chmod 600 ~/github_access/id_midnghtsapphire
chmod 644 ~/github_access/id_midnghtsapphire.pub

# Configure Git with inclusive, descriptive settings
git config --global user.name "Claw (OpenClaw Accessibility Assistant)"
git config --global user.email "claw@openclaw-midnghtsapphire"
git config --global core.accessmode "inclusive"

# Create a comprehensive repository cloning script
cat > ~/github_access/clone_repositories.sh << 'EOL'
#!/bin/bash

# Autonomous Repository Cloning Strategy
CRITICAL_REPOS=(
    "Universal-OZ"
    "SSRN-AUTOMATION"
    "the-alt-text"
    "Neurooz"
    "code-review-mcp-server"
    "Mechatronopolis"
    "affiliate-marketing-system"
    "steel-white"
    "premolt"
    "rags"
    "oz-prompt-library"
    "Meetaudreyevans"
)

# Create base workspace
mkdir -p ~/workspace/github/MIDNGHTSAPPHIRE
cd ~/workspace/github/MIDNGHTSAPPHIRE

# Clone repositories with retry mechanism
for repo in "${CRITICAL_REPOS[@]}"; do
    echo "Cloning: $repo"
    git clone "https://github.com/MIDNGHTSAPPHIRE/${repo}.git" || \
    (sleep 5 && git clone "https://github.com/MIDNGHTSAPPHIRE/${repo}.git")
done

# List cloned repositories
ls -l
EOL

chmod +x ~/github_access/clone_repositories.sh

# Output public key for manual GitHub addition
cat ~/github_access/id_midnghtsapphire.pub