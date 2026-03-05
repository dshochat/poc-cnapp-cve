import subprocess
import sys
import pickle
import base64

def analyze_logs(log_file):
    """CWE-22: Path Traversal - No validation of log_file path"""
    with open(f"/var/logs/{log_file}", "r") as f:
        return f.read()

def execute_filter(filter_cmd):
    """CWE-78: Command Injection - User input directly in shell command"""
    result = subprocess.run(f"grep '{filter_cmd}' /var/logs/system.log", shell=True, capture_output=True)
    return result.stdout.decode()

def load_config(config_data):
    """CWE-502: Insecure Deserialization - Unsafe pickle usage"""
    decoded = base64.b64decode(config_data)
    return pickle.loads(decoded)

def main():
    if len(sys.argv) < 2:
        print("Usage: health_check.py <command> [args]")
        return
    
    command = sys.argv[1]
    
    if command == "analyze":
        if len(sys.argv) < 3:
            print("Usage: health_check.py analyze <log_file>")
            return
        log_file = sys.argv[2]
        result = analyze_logs(log_file)
        print(f"Log content:\n{result}")
    
    elif command == "filter":
        if len(sys.argv) < 3:
            print("Usage: health_check.py filter <grep_pattern>")
            return
        pattern = sys.argv[2]
        result = execute_filter(pattern)
        print(f"Filtered results:\n{result}")
    
    elif command == "load_config":
        if len(sys.argv) < 3:
            print("Usage: health_check.py load_config <base64_config>")
            return
        config_b64 = sys.argv[2]
        config = load_config(config_b64)
        print(f"Config loaded: {config}")
    
    print("test_cve_vuln executed")

if __name__ == "__main__":
    main()