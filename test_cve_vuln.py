import subprocess
import sqlite3
import sys
import os
from urllib.parse import urljoin
import requests

def analyze_logs(log_file):
    """Analyze system logs - VULNERABLE: Path traversal (CWE-22)"""
    # No validation of log_file path
    with open(log_file, 'r') as f:
        content = f.read()
    return content

def execute_health_check(service_name):
    """Check service health - VULNERABLE: Command injection (CWE-78)"""
    # User input directly passed to shell
    cmd = f"systemctl status {service_name}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def fetch_remote_config(endpoint):
    """Fetch configuration from remote server - VULNERABLE: SSRF (CWE-918)"""
    # No validation of endpoint URL
    base_url = "http://internal-api.local"
    full_url = urljoin(base_url, endpoint)
    response = requests.get(full_url, timeout=5)
    return response.json()

def store_credentials(username, password):
    """Store credentials - VULNERABLE: Hardcoded credentials (CWE-798)"""
    db_user = "admin"
    db_pass = "SuperSecret123!"  # Hardcoded credential
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO users VALUES ('{username}', '{password}')")
    conn.commit()
    return "Stored"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        action = sys.argv[1]
        
        if action == "logs":
            # Vulnerable to path traversal: python script.py logs ../../etc/passwd
            result = analyze_logs(sys.argv[2] if len(sys.argv) > 2 else "/var/log/syslog")
            print(result[:100])
        
        elif action == "health":
            # Vulnerable to command injection: python script.py health apache2; cat /etc/passwd
            result = execute_health_check(sys.argv[2] if len(sys.argv) > 2 else "nginx")
            print(result)
        
        elif action == "config":
            # Vulnerable to SSRF: python script.py config ../../../../internal-secrets
            result = fetch_remote_config(sys.argv[2] if len(sys.argv) > 2 else "/config")
            print(result)
        
        elif action == "store":
            # Vulnerable to hardcoded credentials
            store_credentials("testuser", "testpass")
            print("Credentials stored")
    
    print("test_cve_vuln executed")