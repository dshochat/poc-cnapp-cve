#!/usr/bin/env python3
"""test_cve_vuln.py - Intentionally vulnerable script for CVE scanner testing.

Contains SQL injection via string formatting and command injection via os.system.
DO NOT deploy to production. Exists solely for EchoDefense scanner validation.
"""
import os
import sqlite3
import sys


def get_user(db_path, username):
    """SQL injection via string formatting (CWE-89)."""
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM users WHERE name = '%s'" % username
    return conn.execute(query).fetchall()


def run_diagnostic(host):
    """Command injection via os.system (CWE-78)."""
    os.system("ping -c 1 " + host)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_diagnostic(sys.argv[1])
    print("test_cve_vuln executed")

# Run ID: 1c1ec41dbbcf
