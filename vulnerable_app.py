#!/usr/bin/env python3
"""
LogScope - Lightweight Log Viewer Utility
==========================================
A simple CLI tool for operations teams to quickly inspect application log files
from a designated log storage directory.

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
    """Read and display the contents of a log file from the log storage directory."""
    # Construct the full path to the requested log file
    # NOTE: os.path.join silently discards base_dir when filename is absolute,
    # and does not sanitize ".." components — this is the vulnerability (CWE-22)
    log_path = os.path.join(BASE_LOG_DIR, filename)

    print(f"[LogScope] Resolving log path: {log_path}")
    print("-" * 60)

    try:
        with open(log_path, "r") as f:
            contents = f.read()
        print(contents)
    except FileNotFoundError:
        print(f"[ERROR] Log file not found: {log_path}")
        sys.exit(1)
    except PermissionError:
        print(f"[ERROR] Permission denied when reading: {log_path}")
        sys.exit(1)

    print("-" * 60)
    print(f"[LogScope] End of log: {filename}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python vulnerable_app.py <log_filename>")
        sys.exit(1)

    user_input = sys.argv[1]
    view_log(user_input)
    print("vulnerable_app executed")
# Run ID: cb467839f3fc
