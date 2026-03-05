import subprocess
import sqlite3
import sys
from pathlib import Path

# Simulated log analyzer utility
DB_PASSWORD = "admin123"  # CWE-798: Hardcoded credentials

def parse_log_file(filepath):
    """CWE-22: Path traversal vulnerability"""
    base_dir = "/var/logs/"
    # No validation of filepath - allows traversal
    full_path = Path(base_dir) / filepath
    try:
        with open(full_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "File not found"

def search_logs(user_input):
    """CWE-89: SQL injection vulnerability"""
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE logs (id INTEGER, message TEXT)")
    cursor.execute("INSERT INTO logs VALUES (1, 'error occurred')")
    
    # Direct string concatenation allows SQL injection
    query = f"SELECT * FROM logs WHERE message LIKE '%{user_input}%'"
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except sqlite3.Error as e:
        return str(e)
    finally:
        conn.close()

def filter_logs(filter_cmd):
    """CWE-78: Command injection vulnerability"""
    # Unsanitized user input passed to shell
    cmd = f"grep -i '{filter_cmd}' /var/log/syslog"
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)

def check_service_health(service_name):
    """CWE-918: SSRF vulnerability"""
    # User input used directly in URL without validation
    url = f"http://localhost:8080/api/{service_name}/health"
    import urllib.request
    try:
        response = urllib.request.urlopen(url, timeout=2)
        return response.read().decode()
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        if cmd == "parse":
            print(parse_log_file(sys.argv[2] if len(sys.argv) > 2 else "app.log"))
        elif cmd == "search":
            print(search_logs(sys.argv[2] if len(sys.argv) > 2 else "error"))
        elif cmd == "filter":
            print(filter_logs(sys.argv[2] if len(sys.argv) > 2 else "failed"))
        elif cmd == "health":
            print(check_service_health(sys.argv[2] if len(sys.argv) > 2 else "api"))
    print("test_cve_vuln executed")