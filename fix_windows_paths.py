"""
fix_windows_paths.py

Script to detect and fix Windows-incompatible paths in the agent data directories.

This script can:
1. Scan for directories with colons in their names
2. Rename them to use underscores instead
3. Generate a report of fixed issues

Usage:
    python fix_windows_paths.py --scan
    python fix_windows_paths.py --fix
    python fix_windows_paths.py --report
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Tuple
import argparse


def find_colon_paths(root_dir: str = "data") -> List[Tuple[str, str]]:
    """
    Find all directories/files with colons in their names under agent_data directories.

    Args:
        root_dir: Root directory to search (default: "data")

    Returns:
        List of tuples: (old_path, suggested_new_path)
    """
    problematic = []
    root_path = Path(root_dir)

    if not root_path.exists():
        return problematic

    # Find all agent_data directories
    for agent_data_dir in root_path.glob("agent_data*"):
        if agent_data_dir.is_dir():
            # Find all log directories
            for log_dir in agent_data_dir.glob("*/log/*"):
                if ":" in log_dir.name or ":" in str(log_dir):
                    # Suggest new name with underscores
                    new_name = log_dir.name.replace(":", "_").replace(" ", "_")
                    new_path = log_dir.parent / new_name
                    problematic.append((str(log_dir), str(new_path)))

    return problematic


def scan_issues(root_dir: str = "data") -> None:
    """Scan and report Windows-incompatible paths."""
    issues = find_colon_paths(root_dir)

    if not issues:
        print("[OK] No Windows-incompatible paths found!")
        return

    print(f"Found {len(issues)} problematic path(s):")
    print("=" * 60)
    for old_path, new_path in issues:
        print(f"\n[DIR] {old_path}")
        print(f"   -> {new_path}")


def fix_paths(root_dir: str = "data", dry_run: bool = False) -> int:
    """
    Rename directories to use underscores instead of colons.

    Args:
        root_dir: Root directory to search
        dry_run: If True, only show what would be done

    Returns:
        Number of paths fixed
    """
    issues = find_colon_paths(root_dir)

    if not issues:
        print("[OK] No Windows-incompatible paths found!")
        return 0

    if dry_run:
        print(f"Would fix {len(issues)} path(s):")
        print("=" * 60)
        for old_path, new_path in issues:
            print(f"{old_path} -> {new_path}")
        return len(issues)

    fixed = 0
    errors = []

    for old_path, new_path in issues:
        try:
            if os.path.exists(old_path):
                print(f"Renaming: {old_path}")
                print(f"      -> {new_path}")
                os.rename(old_path, new_path)
                fixed += 1
                print("  [OK] Done")
            else:
                print(f"[WARN] Path not found: {old_path}")
        except Exception as e:
            errors.append((old_path, str(e)))
            print(f"[ERROR] Error renaming {old_path}: {e}")

    print("\n" + "=" * 60)
    print(f"Fixed: {fixed} path(s)")
    if errors:
        print(f"Errors: {len(errors)}")
        for path, error in errors:
            print(f"  - {path}: {error}")

    return fixed


def generate_report(root_dir: str = "data") -> str:
    """Generate a detailed report of Windows-incompatible paths."""
    issues = find_colon_paths(root_dir)

    report = []
    report.append("Windows Path Compatibility Report")
    report.append("=" * 60)
    report.append("")

    if not issues:
        report.append("[OK] No Windows-incompatible paths found!")
        report.append("")
        report.append("All directory names are Windows-compatible.")
    else:
        report.append(f"Found {len(issues)} problematic path(s):")
        report.append("")

        for old_path, new_path in issues:
            report.append(f"[DIR] {old_path}")
            report.append(f"   -> {new_path}")
            report.append("")

        report.append("Issue: Windows does not allow colons (:) in file paths")
        report.append("Solution: Replace colons with underscores (_)")

    report.append("")
    report.append("=" * 60)

    return "\n".join(report)


def check_code_fixes() -> None:
    """Check if the code has been fixed to prevent future issues."""
    print("\nChecking code fixes...")
    print("=" * 60)

    agent_files = [
        "agent/base_agent/base_agent.py",
        "agent/base_agent_astock/base_agent_astock.py",
        "agent/base_agent_crypto/base_agent_crypto.py",
    ]

    all_fixed = True
    for file_path in agent_files:
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if '.replace(":", "_")' in content or ".replace(':', '_')" in content:
                    print(f"[OK] {file_path}")
                else:
                    print(f"[FAIL] {file_path} - Missing colon replacement fix")
                    all_fixed = False
        else:
            print(f"[WARN] {file_path} - Not found")

    print("=" * 60)
    if all_fixed:
        print("[OK] All agent files have been fixed to prevent future issues")
    else:
        print("[WARN] Some files need the .replace(':', '_') fix in _setup_logging")


def main():
    parser = argparse.ArgumentParser(
        description="Fix Windows-incompatible paths in agent data directories"
    )
    parser.add_argument(
        "--scan", action="store_true", help="Scan for problematic paths"
    )
    parser.add_argument(
        "--fix", action="store_true", help="Fix problematic paths (rename directories)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be fixed without making changes",
    )
    parser.add_argument(
        "--report", action="store_true", help="Generate detailed report"
    )
    parser.add_argument(
        "--root-dir", default="data", help="Root directory to scan (default: data)"
    )
    parser.add_argument(
        "--check-code",
        action="store_true",
        help="Check if code has been fixed to prevent future issues",
    )

    args = parser.parse_args()

    # Default action: scan
    if not (args.scan or args.fix or args.report or args.check_code):
        args.scan = True

    if args.check_code:
        check_code_fixes()

    if args.scan:
        scan_issues(args.root_dir)

    if args.fix:
        fix_paths(args.root_dir, dry_run=args.dry_run)

    if args.report:
        print(generate_report(args.root_dir))


if __name__ == "__main__":
    main()
