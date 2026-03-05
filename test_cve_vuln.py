import subprocess
import pickle
import sys

def process_log_file(filename):
    # CWE-22: Path Traversal vulnerability
    with open(filename, 'r') as f:
        lines = f.readlines()
    return lines

def execute_health_check(service_name):
    # CWE-78: Command Injection vulnerability
    cmd = f"systemctl status {service_name}"
    result = subprocess.run(cmd, shell=True, capture_output=True)
    return result.stdout.decode()

def load_config(config_data):
    # CWE-502: Insecure Deserialization vulnerability
    return pickle.loads(config_data)

def check_system_health():
    print("System Health Checker v1.0")
    
    # User input without validation
    log_file = input("Enter log file path: ")
    service = input("Enter service name to check: ")
    
    try:
        logs = process_log_file(log_file)
        print(f"Processed {len(logs)} log lines")
    except Exception as e:
        print(f"Error reading log: {e}")
    
    try:
        status = execute_health_check(service)
        print(f"Service status: {status[:100]}")
    except Exception as e:
        print(f"Error checking service: {e}")

if __name__ == "__main__":
    check_system_health()
    print("test_cve_vuln executed")