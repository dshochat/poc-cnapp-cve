import subprocess
import sqlite3
import sys
import os
import pickle

def analyze_logs(log_file):
    # CWE-22: Path Traversal - no validation of log_file path
    with open(log_file, 'r') as f:
        return f.read()

def process_config(user_input):
    # CWE-78: Command Injection - unsanitized user input in shell command
    result = subprocess.run(f"grep 'error' {user_input}", shell=True, capture_output=True)
    return result.stdout.decode()

def load_cache(cache_file):
    # CWE-502: Insecure Deserialization - pickle without validation
    with open(cache_file, 'rb') as f:
        return pickle.load(f)

def health_check(service_name):
    # CWE-78: Command Injection - service_name directly in shell command
    cmd = f"systemctl status {service_name}"
    os.system(cmd)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: utility.py <command> <arg>")
        sys.exit(1)
    
    command = sys.argv[1]
    arg = sys.argv[2] if len(sys.argv) > 2 else ""
    
    if command == "analyze":
        print(analyze_logs(arg))
    elif command == "process":
        print(process_config(arg))
    elif command == "load":
        print(load_cache(arg))
    elif command == "check":
        health_check(arg)
    
    print("test_cve_vuln executed")