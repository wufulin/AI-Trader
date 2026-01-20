#!/bin/bash
# fix_windows_paths.sh
# Script to fix Windows-incompatible paths in git history
# Run this on Linux/WSL, NOT on Windows directly

set -e

echo "========================================="
echo "Fix Windows Path Compatibility Issue"
echo "========================================="
echo ""
echo "This script will:"
echo "1. Find all directories with colons in their names"
echo "2. Remove them from git history"
echo "3. Clean up git refs"
echo ""
echo "⚠️  WARNING: This rewrites git history!"
echo "   Only run this if you're the repository maintainer"
echo "   or have permission to force push."
echo ""
read -p "Continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "Aborted."
    exit 0
fi

echo ""
echo "Step 1: Creating backup branch..."
git branch backup-$(date +%Y%m%d-%H%M%S)
echo "✓ Backup branch created"

echo ""
echo "Step 2: Finding problematic paths..."
# Find all paths with colons
git ls-files -s | grep ':' | cut -f 2 > /tmp/colons.txt || true

if [ -s /tmp/colons.txt ]; then
    echo "Found problematic files:"
    cat /tmp/colons.txt
else
    echo "No files with colons in current index."
    echo "Checking history..."
    git log --all --pretty=format: --name-only | sort -u | grep ':' > /tmp/history_colons.txt || true
    if [ -s /tmp/history_colons.txt ]; then
        echo "Found in history:"
        head -20 /tmp/history_colons.txt
    fi
fi

echo ""
echo "Step 3: Removing problematic paths from history..."
# Use filter-repo or filter-branch to remove problematic paths
if command -v git-filter-repo &> /dev/null; then
    echo "Using git-filter-repo..."
    git filter-repo --path-glob 'data/agent_data/*/log/*:*' --invert-paths
else
    echo "Using git filter-branch (slower)..."
    git filter-branch --force --index-filter \
        'git rm --cached --ignore-unmatch -r data/agent_data/*/log/*:* 2>/dev/null || true' \
        --prune-empty --tag-name-filter cat -- --all
fi

echo "✓ Paths removed from history"

echo ""
echo "Step 4: Cleaning up git objects..."
git reflog expire --expire=now --all
git gc --prune=now --aggressive
echo "✓ Git cleanup complete"

echo ""
echo "Step 5: Checking for remaining issues..."
# Check if any colons remain
if git ls-files -s | grep -q ':'; then
    echo "⚠️  Warning: Some files with colons still exist in the current index"
    git ls-files -s | grep ':'
else
    echo "✓ No colons in current index"
fi

echo ""
echo "========================================="
echo "Cleanup Complete!"
echo "========================================="
echo ""
echo "To apply these changes to the remote repository:"
echo ""
echo "1. Review the changes:"
echo "   git log --oneline"
echo ""
echo "2. Force push to all branches:"
echo "   git push origin --force --all"
echo "   git push origin --force --tags"
echo ""
echo "⚠️  WARNING: Force pushing will rewrite history"
echo "   Make sure all collaborators are aware"
echo ""
