#!/usr/bin/env python3
"""
LogStream - Lightweight CLI Log Viewer
Quickly view application log files from the centralized log store.

Usage: python vulnerable_app.py <log_filename>
Example: python vulnerable_app.py app.log
"""

import os
import sys


LOG_STORE_DIR = "/var/log/logstream"


def view_log(filename):
    """Retrieve and display a log file from the log store directory."""
    # Construct the full path to the requested log file
    # NOTE: os.path.join will discard the base if filename is absolute,
    # and does NOT sanitize ".." traversal components
    filepath = os.path.join(LOG_STORE_DIR, filename)

    print(f"[LogStream] Resolving log path: {filepath}")

    try:
        with open(filepath, "r") as f:
            contents = f.read()
        print("=" * 60)
        print(f"  LOG FILE: {filename}")
        print("=" * 60)
        print(contents)
        print("=" * 60)
    except FileNotFoundError:
        print(f"[LogStream] Error: Log file '{filename}' not found in store.")
    except PermissionError:
        print(f"[LogStream] Error: Permission denied reading '{filepath}'.")
    except Exception as e:
        print(f"[LogStream] Unexpected error: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python vulnerable_app.py <log_filename>")
        print("Example: python vulnerable_app.py application.log")
        sys.exit(1)

    user_input = sys.argv[1]
    view_log(user_input)
    print("vulnerable_app executed")
# Run ID: 7dde5a99cb2f
