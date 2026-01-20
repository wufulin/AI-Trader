# Fix Windows Git Clone Issue - Invalid Argument

## Problem Summary

Windows systems do not allow colons (`:`) in file paths. The repository history contains directories like:
```
data/agent_data/MiniMax-M2/log/2025-10-01 15:00:00/log.jsonl
```

This causes `git clone` to fail on Windows with:
```
fatal: cannot create directory at 'data/agent_data/MiniMax-M2/log/2025-10-01 15:00:00': Invalid argument
```

## Solution

### Option 1: Remove Problematic Files from Git History (Recommended)

Run this script in the repository root:

```bash
#!/bin/bash
# fix_windows_paths.sh - Remove problematic paths from git history

# Find all log directories with colons in their names
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch -r data/agent_data/*/log/*:*' \
  --prune-empty --tag-name-filter cat -- --all

# Clean up
git reflog expire --expire=now --all
git gc --prune=now --aggressive

# Force push (CAUTION: This rewrites history)
git push origin --force --all
git push origin --force --tags
```

### Option 2: Use Git Sparse Checkout (For Windows Users)

Windows users can clone with sparse checkout to skip problematic files:

```bash
# Clone without checkout
git clone --no-checkout https://github.com/HKUDS/AI-Trader.git
cd AI-Trader

# Enable sparse checkout
git sparse-checkout init

# Exclude problematic log directories with colons
git sparse-checkout set '/*' '!data/agent_data/*/log/*:*'

# Checkout the rest
git checkout
```

### Option 3: Use WSL or Linux Environment

Clone and fix the repository on Linux/WSL, then Windows users can use the fixed version:

```bash
# On Linux/WSL
git clone https://github.com/HKUDS/AI-Trader.git
cd AI-Trader

# Find and rename problematic directories
find data/agent_data -type d -name '*:*' -exec bash -c 'mv "$1" "$(echo "$1" | tr : _)"' _ {} \;

# Commit the changes
git add .
git commit -m "Fix: Replace colons with underscores in directory names for Windows compatibility"
git push
```

## Prevention

The code has already been fixed to prevent this issue in the future:
- `agent/base_agent/base_agent.py:438` - Uses `.replace(":", "_")`
- `agent/base_agent_astock/base_agent_astock.py:343` - Uses `.replace(":", "_")`
- `agent/base_agent_crypto/base_agent_crypto.py:322` - Uses `.replace(":", "_")`

All new log directories will use underscores instead of colons:
```
data/agent_data/MiniMax-M2/log/2025-10-01_15_00_00/log.jsonl
```

## For Repository Maintainers

To completely fix this issue for all users:

1. **On Linux/WSL**, clone the repository
2. Run the cleanup script to remove/rename problematic files
3. Force push to update the main branch
4. Windows users can then clone normally

## For Windows Users (Immediate Workaround)

If you need to use this repository immediately:

1. Use GitHub DevSpaces or Codespaces
2. Use WSL (Windows Subsystem for Linux)
3. Use a Docker container
4. Wait for the repository maintainers to fix the git history
