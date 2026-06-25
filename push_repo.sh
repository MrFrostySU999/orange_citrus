#!/bin/bash
set -e

# Check if username was passed as an argument
if [ -z "$1" ]; then
    echo "Error: You must provide your GitHub username."
    echo "Usage: ./push_repo.sh YOUR_USERNAME"
    exit 1
fi

USERNAME="$1"
REPO_NAME="orange_juice_repo"

echo "=== Non-Interactive Git Setup ==="

if [ ! -d ".git" ]; then
    git init
fi

git add .

if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    git commit -m "Initial commit"
fi

git branch -M main

# Set the remote URL directly using the argument
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com"

echo "Pushing code for user: $USERNAME..."
git push -u origin main
echo "=== Complete! ==="
