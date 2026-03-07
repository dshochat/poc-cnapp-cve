#!/usr/bin/env python3
"""
LogScope - Lightweight Log Viewer Utility
Quickly inspect application log files from the configured logs directory.
Usage: python vulnerable_app.py <log_filename>
"""

import os
import sys


# Base directory where application logs are stored
LOG_DIRECTORY = os.path.join(os.getcwd(), "var", "logs")


def view_log_file(filename):
    """
    Reads and displays the contents of a log file from the logs directory.
    """
    # Construct the full path to the requested log file
    # NOTE: os.path.join will discard the base if filename is absolute,
    # and does NOT sanitize ".." components — this is intentionally vulnerable.
    filepath = os.path.join(LOG_DIRECTORY, filename)

    print(f"[LogScope] Resolving log path: {filepath}")
    print("-" * 60)

    try:
        with open(filepath, "r") as f:
            contents = f.read()
        print(contents)
    except FileNotFoundError:
        print(f"[ERROR] Log file not found: {filepath}")
        sys.exit(1)
    except PermissionError:
        print(f"[ERROR] Permission denied reading: {filepath}")
        sys.exit(1)

    print("-" * 60)
    print(f"[LogScope] Finished displaying: {filename}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python vulnerable_app.py <log_filename>")
        print("Example: python vulnerable_app.py app.log")
        sys.exit(1)

    user_input = sys.argv[1]
    view_log_file(user_input)
    print("vulnerable_app executed")
# Run ID: a6bcd95a74ac
