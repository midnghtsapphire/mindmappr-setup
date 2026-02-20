#!/bin/bash

# GitHub Deployment and Management Script for MIDNGHTSAPPHIRE

# Domains to deploy
DOMAINS=(
    "meetaudreyevans.com"
    "yumyumcode.com"
    "growlingeyes.com"
    "truthslayer.com"
    "glowstarlabs.com"
    "audreyevansofficial.com"
    "reesereviews.com"
)

# Function to clone and setup repository
setup_repository() {
    local domain=$1
    local repo_name=$(echo "$domain" | sed 's/\.com//')
    
    # Clone repository
    git clone "https://github.com/MIDNGHTSAPPHIRE/${repo_name}.git"
    
    # Enter repository directory
    cd "${repo_name}"
    
    # Configure GitHub Pages
    gh repo deploy --source docs/
    
    # Set up custom domain
    echo "$domain" > CNAME
    
    # Return to parent directory
    cd ..
}

# Main deployment process
main() {
    # Create GitHub Pages directory
    mkdir -p ~/github-pages
    cd ~/github-pages
    
    # Deploy each domain
    for domain in "${DOMAINS[@]}"; do
        setup_repository "$domain"
    done
    
    # Accessibility and performance audit
    npm install -g lighthouse
    for domain in "${DOMAINS[@]}"; do
        lighthouse "https://${domain}" --view
    done
}

# Run the deployment
main