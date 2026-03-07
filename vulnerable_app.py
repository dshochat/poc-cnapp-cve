#!/usr/bin/env python3
"""
LogScope - Lightweight Log Viewer Utility
==========================================
A simple CLI tool for operations teams to quickly inspect application log files
stored under the designated logs directory.

Usage:
    python vulnerable_app.py <log_filename>

Example:
    python vulnerable_app.py app.log
    python vulnerable_app.py errors/2024-01-15.log
"""

import os
import sys


BASE_LOG_DIR = os.path.join(os.getcwd(), "logs")


def view_log(log_name):
    """Read and display the contents of the requested log file."""
    # Construct the full path to the requested log file
    # NOTE: This is intentionally vulnerable — os.path.join does NOT sanitize
    # directory traversal sequences like "../../" in user input, and if the
    # user_input starts with "/" it replaces the base entirely.
    log_path = os.path.join(BASE_LOG_DIR, log_name)

    print(f"[LogScope] Base directory : {BASE_LOG_DIR}")
    print(f"[LogScope] Requested file : {log_name}")
    print(f"[LogScope] Resolved path  : {log_path}")
    print("-" * 60)

    try:
        with open(log_path, "r") as f:
            contents = f.read()
        print(contents)
    except FileNotFoundError:
        print(f"[ERROR] Log file not found: {log_path}")
    except PermissionError:
        print(f"[ERROR] Permission denied: {log_path}")
    except Exception as e:
        print(f"[ERROR] Could not read log file: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python vulnerable_app.py <log_filename>")
        sys.exit(1)

    user_input = sys.argv[1]
    view_log(user_input)
    print("vulnerable_app executed")
# Run ID: 85dd8d401881
