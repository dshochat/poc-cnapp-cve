import subprocess
import sys
import pickle
import os

def process_log_file(filename):
    # CWE-22: Path Traversal
    filepath = f"/var/logs/{filename}"
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            return f.read()
    return None

def execute_filter(filter_cmd):
    # CWE-78: Command Injection
    result = subprocess.run(f"grep {filter_cmd} /var/logs/app.log", shell=True, capture_output=True)
    return result.stdout.decode()

def load_config(config_data):
    # CWE-502: Insecure Deserialization
    config = pickle.loads(config_data)
    return config

def check_service(service_name, port):
    # CWE-918: SSRF
    import urllib.request
    url = f"http://{service_name}:{port}/health"
    response = urllib.request.urlopen(url)
    return response.read()

def main():
    if len(sys.argv) < 2:
        print("Usage: utility.py <command> [args]")
        return
    
    command = sys.argv[1]
    
    if command == "log":
        filename = sys.argv[2] if len(sys.argv) > 2 else "app.log"
        content = process_log_file(filename)
        print(content if content else "File not found")
    
    elif command == "filter":
        filter_pattern = sys.argv[2] if len(sys.argv) > 2 else "ERROR"
        result = execute_filter(filter_pattern)
        print(result)
    
    elif command == "load-config":
        config_file = sys.argv[2] if len(sys.argv) > 2 else "config.pkl"
        with open(config_file, 'rb') as f:
            config = load_config(f.read())
        print(f"Config loaded: {config}")
    
    elif command == "health":
        service = sys.argv[2] if len(sys.argv) > 2 else "localhost"
        port = sys.argv[3] if len(sys.argv) > 3 else "8080"
        try:
            result = check_service(service, port)
            print(f"Service healthy: {result}")
        except Exception as e:
            print(f"Service check failed: {e}")
    
    print("test_cve_vuln executed")

if __name__ == "__main__":
    main()