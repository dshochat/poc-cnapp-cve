#!/usr/bin/env python3
"""
LogStream - Lightweight CLI Log Viewer
Quickly inspect application log files from the configured logs directory.

Usage:
    python vulnerable_app.py <log_filename>

Examples:
    python vulnerable_app.py app.log
    python vulnerable_app.py errors/2024-01-15.log
"""

import os
import sys


LOGS_BASE_DIR = "/var/log/myapp"


def view_log(filename):
    """Read and display the contents of the requested log file."""
    # Build the full path to the requested log file
    log_path = os.path.join(LOGS_BASE_DIR, filename)

    print(f"[LogStream] Requesting log: {filename}")
    print(f"[LogStream] Resolved path: {log_path}")
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

    print("-" * 60)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python vulnerable_app.py <log_filename>")
        sys.exit(1)

    user_input = sys.argv[1]
    view_log(user_input)
    print("vulnerable_app executed")
# Run ID: 99332c3383b5
