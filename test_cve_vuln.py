import subprocess
import sqlite3
import sys
import os

# Vulnerable Config Manager
PASSWORD = "admin123"  # CWE-798: Hardcoded Credentials

def process_log_file(filename):
    """Process log file - CWE-22: Path Traversal Vulnerability"""
    # No validation of filename - allows directory traversal
    try:
        with open(filename, 'r') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def execute_filter(filter_cmd):
    """Execute filter command - CWE-78: Command Injection Vulnerability"""
    # User input directly passed to shell
    try:
        result = subprocess.run(f"grep {filter_cmd} /var/log/system.log", 
                              shell=True, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        print(f"Error executing filter: {e}")
        return None

def query_database(user_id):
    """Query database - CWE-89: SQL Injection Vulnerability"""
    # User input directly concatenated into SQL query
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    return cursor.fetchall()

def check_credentials(username, password):
    """Check if credentials match hardcoded values"""
    if username == "admin" and password == PASSWORD:
        return True
    return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <command> [args]")
        return
    
    command = sys.argv[1]
    
    if command == "read":
        if len(sys.argv) > 2:
            content = process_log_file(sys.argv[2])
            print(content if content else "File not found")
    
    elif command == "filter":
        if len(sys.argv) > 2:
            result = execute_filter(sys.argv[2])
            print(result if result else "No matches")
    
    elif command == "query":
        if len(sys.argv) > 2:
            result = query_database(sys.argv[2])
            print(result if result else "No results")
    
    elif command == "auth":
        if len(sys.argv) > 3:
            if check_credentials(sys.argv[2], sys.argv[3]):
                print("Authentication successful")
            else:
                print("Authentication failed")
    
    print("test_cve_vuln executed")

if __name__ == "__main__":
    main()