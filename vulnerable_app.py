#!/usr/bin/env python3
"""
LogScope - Lightweight Log Viewer Utility
==========================================
A simple CLI tool for operations teams to quickly inspect application
log files stored under the designated logs directory.

Usage:
    python vulnerable_app.py <log_filename>

Example:
    python vulnerable_app.py nginx/access.log
"""

import os
import sys


BASE_LOG_DIR = "/var/log/logscope"


def view_log(filename):
    """Read and display the contents of the requested log file."""
    # Construct the full path to the requested log file
    # NOTE: os.path.join does NOT sanitize directory traversal sequences
    filepath = os.path.join(BASE_LOG_DIR, filename)

    print(f"[LogScope] Requesting log file: {filename}")
    print(f"[LogScope] Resolved path:       {filepath}")
    print("-" * 60)

    try:
        with open(filepath, "r") as f:
            contents = f.read()
        print(contents)
    except FileNotFoundError:
        print(f"[ERROR] Log file not found: {filepath}")
    except PermissionError:
        print(f"[ERROR] Permission denied: {filepath}")
    except Exception as e:
        print(f"[ERROR] Could not read log file: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python vulnerable_app.py <log_filename>")
        print("Example: python vulnerable_app.py app/error.log")
        sys.exit(1)

    user_input = sys.argv[1]
    view_log(user_input)
    print("vulnerable_app executed")
# Run ID: b24e929be517
