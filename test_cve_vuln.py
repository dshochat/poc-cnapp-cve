import subprocess
import sqlite3
import sys
import os

def analyze_logs(log_file):
    # CWE-22: Path Traversal vulnerability
    file_path = f"/var/logs/{log_file}"
    with open(file_path, 'r') as f:
        return f.read()

def search_logs(search_term):
    # CWE-78: Command Injection vulnerability
    command = f"grep '{search_term}' /var/logs/app.log"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

def store_metric(metric_name, metric_value):
    # CWE-89: SQL Injection vulnerability
    conn = sqlite3.connect('/tmp/metrics.db')
    cursor = conn.cursor()
    query = f"INSERT INTO metrics (name, value) VALUES ('{metric_name}', '{metric_value}')"
    cursor.execute(query)
    conn.commit()
    conn.close()

def get_system_info():
    info = {
        'db_user': 'admin',
        'db_pass': 'SuperSecret123!',  # CWE-798: Hardcoded credentials
        'api_key': 'sk-1234567890abcdef'
    }
    return info

def health_check(hostname):
    # CWE-78: Command Injection via ping
    ping_cmd = f"ping -c 1 {hostname}"
    try:
        subprocess.run(ping_cmd, shell=True, timeout=5)
        return "Host is up"
    except subprocess.TimeoutExpired:
        return "Host is down"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        action = sys.argv[1]
        if action == "analyze":
            result = analyze_logs(sys.argv[2])
            print(result)
        elif action == "search":
            result = search_logs(sys.argv[2])
            print(result)
        elif action == "check":
            result = health_check(sys.argv[2])
            print(result)
    
    print("test_cve_vuln executed")