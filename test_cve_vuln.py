import os
import sys
import pickle
import subprocess
from urllib.parse import urlparse
import requests

class ConfigManager:
    def __init__(self):
        self.config = {}
    
    def load_config(self, user_input):
        # CWE-502: Insecure Deserialization
        serialized_data = user_input.encode()
        self.config = pickle.loads(serialized_data)
        return self.config
    
    def execute_health_check(self, service_name):
        # CWE-78: Command Injection
        command = f"curl http://localhost:8080/{service_name}/health"
        result = subprocess.run(command, shell=True, capture_output=True)
        return result.stdout.decode()
    
    def fetch_remote_config(self, endpoint_url):
        # CWE-918: SSRF
        parsed_url = urlparse(endpoint_url)
        response = requests.get(endpoint_url)
        return response.text
    
    def analyze_log_file(self, log_path):
        # CWE-22: Path Traversal
        log_directory = "/var/logs/"
        full_path = os.path.join(log_directory, log_path)
        with open(full_path, 'r') as f:
            return f.read()

def main():
    manager = ConfigManager()
    
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
        
        try:
            manager.load_config(user_input)
        except Exception as e:
            print(f"Config load error: {e}")
        
        service = sys.argv[2] if len(sys.argv) > 2 else "default"
        try:
            manager.execute_health_check(service)
        except Exception as e:
            print(f"Health check error: {e}")
    
    print("test_cve_vuln executed")

if __name__ == "__main__":
    main()