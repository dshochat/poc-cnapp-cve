#!/usr/bin/env python3
"""
LogScope - Lightweight Log Viewer Utility
==========================================
A simple CLI tool for viewing application log files stored in the
designated logs directory. Useful for quick troubleshooting without
needing to navigate to the log storage path manually.

Usage:
    python vulnerable_app.py <log_filename>

Example:
    python vulnerable_app.py app.log
    python vulnerable_app.py errors/2024-01-15.log
"""

import os
import sys


BASE_LOG_DIR = "/var/log/logscope"


def view_log(filename):
    """Read and display the contents of the requested log file."""
    # Construct the full path to the log file
    log_path = os.path.join(BASE_LOG_DIR, filename)

    print(f"[LogScope] Requesting log file: {filename}")
    print(f"[LogScope] Resolved path: {log_path}")
    print("-" * 60)

    try:
        with open(log_path, "r") as f:
            contents = f.read()
        print(contents)
    except FileNotFoundError:
        print(f"[ERROR] Log file not found: {log_path}")
    except PermissionError:
        print(f"[ERROR] Permission denied reading: {log_path}")
    except Exception as e:
        print(f"[ERROR] Could not read log file: {e}")

    print("-" * 60)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python vulnerable_app.py <log_filename>")
        print("Example: python vulnerable_app.py app.log")
        sys.exit(1)

    user_input = sys.argv[1]
    view_log(user_input)
    print("vulnerable_app executed")
# Run ID: f80f1915303d
