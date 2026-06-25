#!/bin/bash

# Exit immediately if any command fails
set -e

echo "=== Git Repository Auto-Setup ==="

# 1. Initialize Git if not already done
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
else
    echo "Git repository already initialized."
fi

# 2. Stage and commit files
echo "Staging files..."
git add .

# Check if there are changes to commit
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    echo "Committing files..."
    git commit -m "Initial commit from Termux automation script"
else
    echo "No new changes to commit."
fi

# 3. Rename branch to main
echo "Setting default branch to main..."
git branch -M main

# 4. Prompt for GitHub details
echo ""
read -p "Enter your GitHub username: " USERNAME
REPO_NAME="orange_juice_repo"

# 5. Remove existing origin if it exists, then add the new one
git remote remove origin 2>/dev/null || true
echo "Linking to remote: https://github.com"
git remote add origin "https://github.com"

# 6. Reminder message
echo ""
echo "!!! IMPORTANT !!!"
echo "Before proceeding, make sure you created '$REPO_NAME' on github.com."
echo "If prompted for a password, enter your GitHub Personal Access Token (PAT)."
echo "----------------------------------------------------"
read -p "Press [Enter] to push your code now..."

# 7. Push to GitHub
echo "Pushing code to GitHub..."
git push -u origin main

echo "=== Setup Complete! ==="
