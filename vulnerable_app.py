#!/usr/bin/env python3
"""
LogStream - Lightweight Application Log Viewer
================================================
A simple CLI utility for developers to quickly inspect application log files
stored in the project's logs/ directory.

Usage:
    python vulnerable_app.py <log_filename>

Examples:
    python vulnerable_app.py app.log
    python vulnerable_app.py errors/2024-01-15.log
"""

import os
import sys


BASE_LOG_DIR = os.path.join(os.getcwd(), "logs")


def view_log(filename):
    """Read and display the contents of the requested log file."""
    # Construct the full path to the requested log file
    log_path = os.path.join(BASE_LOG_DIR, filename)

    print(f"[LogStream] Base directory : {BASE_LOG_DIR}")
    print(f"[LogStream] Requested file : {filename}")
    print(f"[LogStream] Resolved path  : {log_path}")
    print("-" * 60)

    try:
        with open(log_path, "r") as f:
            contents = f.read()
        print(contents)
    except FileNotFoundError:
        print(f"[ERROR] Log file not found: {log_path}")
        sys.exit(1)
    except PermissionError:
        print(f"[ERROR] Permission denied reading: {log_path}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python vulnerable_app.py <log_filename>")
        print("Example: python vulnerable_app.py app.log")
        sys.exit(1)

    user_input = sys.argv[1]
    view_log(user_input)
    print("vulnerable_app executed")
# Run ID: d8b6b00a318e
