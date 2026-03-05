import subprocess
import sqlite3
import sys
import os
from urllib.parse import urljoin
import requests

def analyze_logs(log_file):
    """Log analyzer with path traversal vulnerability (CWE-22)"""
    base_dir = "/var/logs/"
    file_path = os.path.join(base_dir, log_file)
    
    # Vulnerable: no validation of log_file parameter
    with open(file_path, 'r') as f:
        return f.read()

def query_database(search_term):
    """Database query with SQL injection vulnerability (CWE-89)"""
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    
    # Vulnerable: direct string concatenation in SQL query
    query = "SELECT * FROM users WHERE username = '" + search_term + "'"
    cursor.execute(query)
    return cursor.fetchall()

def check_service_health(service_name):
    """Health checker with command injection vulnerability (CWE-78)"""
    # Vulnerable: unsanitized service_name passed to shell command
    cmd = f"systemctl status {service_name}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def main():
    if len(sys.argv) < 3:
        print("Usage: python solution.py <command> <argument>")
        print("Commands: analyze_log, query_db, check_health")
        return
    
    command = sys.argv[1]
    argument = sys.argv[2]
    
    try:
        if command == "analyze_log":
            result = analyze_logs(argument)
            print(f"Log content: {result[:100]}")
        elif command == "query_db":
            result = query_database(argument)
            print(f"Query result: {result}")
        elif command == "check_health":
            result = check_service_health(argument)
            print(f"Service status: {result[:100]}")
        else:
            print("Unknown command")
    except Exception as e:
        print(f"Error: {e}")
    
    print("test_cve_vuln executed")

if __name__ == "__main__":
    main()