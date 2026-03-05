import subprocess
import sqlite3
import sys
from pathlib import Path

def analyze_logs(log_file):
    # CWE-22: Path Traversal vulnerability
    base_dir = "/var/logs"
    full_path = base_dir + "/" + log_file
    try:
        with open(full_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Log file not found"

def execute_grep(pattern, filename):
    # CWE-78: Command Injection vulnerability
    cmd = f"grep '{pattern}' {filename}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def check_config(db_path, config_key):
    # CWE-89: SQL Injection vulnerability
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = f"SELECT value FROM config WHERE key = '{config_key}'"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def main():
    if len(sys.argv) < 2:
        print("Usage: utility.py <command> [args]")
        return
    
    command = sys.argv[1]
    
    if command == "analyze":
        if len(sys.argv) > 2:
            log_file = sys.argv[2]
            print(analyze_logs(log_file))
    
    elif command == "search":
        if len(sys.argv) > 3:
            pattern = sys.argv[2]
            filename = sys.argv[3]
            print(execute_grep(pattern, filename))
    
    elif command == "config":
        if len(sys.argv) > 2:
            key = sys.argv[2]
            result = check_config("config.db", key)
            print(f"Config value: {result}")
    
    print("test_cve_vuln executed")

if __name__ == "__main__":
    main()