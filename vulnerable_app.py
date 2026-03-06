#!/usr/bin/env python3
"""vulnerable_app.py — Intentionally vulnerable file server.

Contains a Path Traversal vulnerability (CWE-22) via unsafe os.path.join.
DO NOT deploy to production. Exists solely for EchoDefense enforcement testing.
"""
import os
import sys


def read_file(base_dir, user_path):
    """Read a file relative to base_dir — VULNERABLE to path traversal (CWE-22).

    os.path.join discards base_dir when user_path is absolute,
    and '../' sequences escape the intended directory.
    """
    full_path = os.path.join(base_dir, user_path)
    try:
        with open(full_path, "r") as f:
            return f.read()
    except Exception as e:
        return f"Error: {e}"


if __name__ == "__main__":
    if len(sys.argv) > 1:
        base = "/var/www/html"
        result = read_file(base, sys.argv[1])
        print(result)
    else:
        print("Usage: vulnerable_app.py <path>")
    print("vulnerable_app executed")
