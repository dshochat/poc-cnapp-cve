import subprocess
import sqlite3
import sys
import os
import pickle
import base64

def analyze_logs(log_file):
    """CWE-22: Path Traversal vulnerability"""
    log_path = f"/var/logs/{log_file}"
    with open(log_path, 'r') as f:
        return f.read()

def execute_command(user_input):
    """CWE-78: Command Injection vulnerability"""
    cmd = f"grep '{user_input}' /var/log/system.log"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

def load_config(config_data):
    """CWE-502: Insecure Deserialization vulnerability"""
    decoded = base64.b64decode(config_data)
    config = pickle.loads(decoded)
    return config

def check_health(host):
    """CWE-918: SSRF vulnerability"""
    import urllib.request
    url = f"http://{host}:8080/health"
    response = urllib.request.urlopen(url)
    return response.read()

def main():
    if len(sys.argv) < 3:
        print("Usage: utility <command> <argument>")
        return
    
    command = sys.argv[1]
    argument = sys.argv[2]
    
    if command == "analyze":
        print(analyze_logs(argument))
    elif command == "search":
        print(execute_command(argument))
    elif command == "load":
        print(load_config(argument))
    elif command == "health":
        print(check_health(argument))
    
    print("test_cve_vuln executed")

if __name__ == "__main__":
    main()