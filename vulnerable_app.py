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
    python vulnerable_app.py 2024/january/error.log
"""

import os
import sys


# Base directory where all application logs are stored
LOG_BASE_DIR = "/var/log/logscope"


def view_log_file(filename):
    """Read and display the contents of the requested log file."""
    # Construct the full path to the requested log file
    # NOTE: os.path.join does NOT sanitize directory traversal sequences
    # If filename starts with or contains "../", it can escape LOG_BASE_DIR
    file_path = os.path.join(LOG_BASE_DIR, filename)

    print(f"[LogScope] Resolving log path: {file_path}")

    try:
        with open(file_path, "r") as f:
            contents = f.read()
        print(f"[LogScope] --- Begin File: {filename} ---")
        print(contents)
        print(f"[LogScope] --- End File: {filename} ---")
    except FileNotFoundError:
        print(f"[LogScope] ERROR: Log file not found: {file_path}")
    except PermissionError:
        print(f"[LogScope] ERROR: Permission denied: {file_path}")
    except Exception as e:
        print(f"[LogScope] ERROR: Could not read file: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python vulnerable_app.py <log_filename>")
        print("Example: python vulnerable_app.py app.log")
        sys.exit(1)

    user_input = sys.argv[1]
    view_log_file(user_input)
    print("vulnerable_app executed")
# Run ID: 99bd6ff6df49
