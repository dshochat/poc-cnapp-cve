import sqlite3
import subprocess
import sys
import os

def log_analyzer(log_file):
    """Analyze system logs with user input - vulnerable to path traversal"""
    # CWE-22: Path Traversal - no validation of log_file path
    with open(log_file, 'r') as f:
        content = f.read()
    return content

def search_logs(search_term):
    """Search logs using command line tool - vulnerable to command injection"""
    # CWE-78: Command Injection - user input directly in shell command
    cmd = f"grep '{search_term}' /var/log/syslog"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def fetch_user_config(user_id):
    """Fetch user configuration from database - vulnerable to SQL injection"""
    # CWE-89: SQL Injection - user input concatenated into query
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    return cursor.fetchall()

def main():
    if len(sys.argv) < 3:
        print("Usage: python script.py <action> <input>")
        sys.exit(1)
    
    action = sys.argv[1]
    user_input = sys.argv[2]
    
    if action == "analyze":
        try:
            result = log_analyzer(user_input)
            print(f"Log content: {result[:100]}")
        except FileNotFoundError:
            print("Log file not found")
    
    elif action == "search":
        result = search_logs(user_input)
        print(f"Search results: {result}")
    
    elif action == "config":
        result = fetch_user_config(user_input)
        print(f"Config: {result}")
    
    print("test_cve_vuln executed")

if __name__ == "__main__":
    main()