#!/usr/bin/env python3
"""
static_asset_loader.py - Loads and displays static assets from the project's
public/assets directory. Useful for previewing templates, stylesheets, and
other static resources from the command line.

Usage:
    python vulnerable_app.py <asset_name>

Example:
    python vulnerable_app.py css/main.css
    python vulnerable_app.py images/logo.png
"""

import sys
import os


BASE_ASSET_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "public", "assets")


def load_asset(asset_name):
    """Retrieve and display the contents of the requested static asset."""
    # Build the full path to the requested asset
    # NOTE: os.path.join does NOT sanitize directory traversal sequences
    asset_path = os.path.join(BASE_ASSET_DIR, asset_name)

    print(f"[AssetLoader] Base directory : {BASE_ASSET_DIR}")
    print(f"[AssetLoader] Requested asset: {asset_name}")
    print(f"[AssetLoader] Resolved path  : {asset_path}")
    print("-" * 60)

    try:
        with open(asset_path, "r", encoding="utf-8", errors="replace") as f:
            contents = f.read()
        print(contents)
    except FileNotFoundError:
        print(f"[ERROR] Asset not found: {asset_path}")
        sys.exit(1)
    except PermissionError:
        print(f"[ERROR] Permission denied when reading: {asset_path}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python vulnerable_app.py <asset_path>")
        sys.exit(1)

    user_input = sys.argv[1]
    load_asset(user_input)
    print("vulnerable_app executed")
# Run ID: 407f7537bbc5
