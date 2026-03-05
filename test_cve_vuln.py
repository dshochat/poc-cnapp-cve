import subprocess
import pickle
import sys
import os

def parse_log_file(filename):
    # CWE-22: Path Traversal vulnerability
    log_path = f"/var/logs/{filename}"
    try:
        with open(log_path, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return "Log file not found"

def execute_analysis(user_command):
    # CWE-78: Command Injection vulnerability
    result = subprocess.run(f"grep 'ERROR' /var/logs/app.log | {user_command}", 
                           shell=True, capture_output=True, text=True)
    return result.stdout

def load_config(config_data):
    # CWE-502: Insecure Deserialization vulnerability
    return pickle.loads(config_data)

def check_health(service_name):
    # Additional CWE-78: Command Injection in health check
    status = subprocess.run(f"systemctl status {service_name}", 
                           shell=True, capture_output=True, text=True)
    return status.stdout

def main():
    if len(sys.argv) < 2:
        print("Usage: python utility.py <command> [args]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "parse":
        filename = sys.argv[2] if len(sys.argv) > 2 else "app.log"
        print(parse_log_file(filename))
    elif command == "analyze":
        user_cmd = sys.argv[2] if len(sys.argv) > 2 else "cat"
        print(execute_analysis(user_cmd))
    elif command == "health":
        service = sys.argv[2] if len(sys.argv) > 2 else "nginx"
        print(check_health(service))
    else:
        print("Unknown command")
    
    print("test_cve_vuln executed")

if __name__ == "__main__":
    main()