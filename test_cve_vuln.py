import subprocess
import pickle
import sys
import os

def parse_log_file(filepath):
    # CWE-22: Path Traversal - no validation of filepath
    with open(filepath, 'r') as f:
        return f.read()

def execute_filter(user_filter):
    # CWE-78: Command Injection - unsanitized user input in shell command
    command = f"grep '{user_filter}' /var/log/syslog"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout

def load_config(config_data):
    # CWE-502: Insecure Deserialization - unpickling untrusted data
    return pickle.loads(config_data)

def check_system_health(config_bytes):
    print("System Health Checker v1.0")
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        log_path = sys.argv[1]
        try:
            logs = parse_log_file(log_path)
            print(f"Loaded {len(logs)} bytes from log")
        except Exception as e:
            print(f"Error: {e}")
    
    if len(sys.argv) > 2:
        filter_term = sys.argv[2]
        filtered = execute_filter(filter_term)
        print(f"Filtered results:\n{filtered}")
    
    try:
        config = load_config(config_bytes)
        print(f"Config loaded: {config}")
    except Exception as e:
        print(f"Config error: {e}")

if __name__ == "__main__":
    check_system_health(b"")
    print("test_cve_vuln executed")