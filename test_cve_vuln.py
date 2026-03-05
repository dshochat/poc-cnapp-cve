import subprocess
import os
import sqlite3
import sys

def analyze_logs(log_file):
    """Vulnerable log analyzer with path traversal and command injection"""
    # CWE-22: Path Traversal - no validation of log_file path
    with open(log_file, 'r') as f:
        content = f.read()
    
    # CWE-78: Command Injection - unsanitized grep command
    search_term = input("Enter search term: ")
    cmd = f"grep '{search_term}' {log_file}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)

def query_database(user_input):
    """Vulnerable database query"""
    # CWE-89: SQL Injection - direct string concatenation
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE username = '{user_input}'")
    return cursor.fetchall()

def fetch_remote_config(url):
    """Vulnerable remote fetcher"""
    # CWE-918: SSRF - no URL validation
    import urllib.request
    try:
        response = urllib.request.urlopen(url, timeout=5)
        return response.read().decode()
    except Exception as e:
        return f"Error: {e}"

def main():
    if len(sys.argv) < 2:
        print("Usage: utility.py [analyze|query|fetch]")
        return
    
    action = sys.argv[1]
    
    if action == "analyze" and len(sys.argv) > 2:
        analyze_logs(sys.argv[2])
    elif action == "query" and len(sys.argv) > 2:
        print(query_database(sys.argv[2]))
    elif action == "fetch" and len(sys.argv) > 2:
        print(fetch_remote_config(sys.argv[2]))

if __name__ == "__main__":
    main()
    print("test_cve_vuln executed")