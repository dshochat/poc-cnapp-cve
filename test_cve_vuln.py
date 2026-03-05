import subprocess
import pickle
import sys
from pathlib import Path

def log_analyzer(log_file):
    """Analyzes log files - contains path traversal vulnerability"""
    # CWE-22: Path Traversal - no validation of log_file path
    with open(log_file, 'r') as f:
        content = f.read()
    return content

def execute_filter(filter_cmd):
    """Executes filter command on logs - contains command injection"""
    # CWE-78: Command Injection - directly using user input in shell command
    result = subprocess.run(f"grep {filter_cmd} /var/log/system.log", 
                          shell=True, capture_output=True, text=True)
    return result.stdout

def load_config(config_data):
    """Loads configuration from pickled data - insecure deserialization"""
    # CWE-502: Insecure Deserialization - unsafe pickle.loads
    config = pickle.loads(config_data)
    return config

def check_health(service_url):
    """Checks service health - SSRF vulnerability"""
    # CWE-918: SSRF - directly using user input in request URL
    import urllib.request
    try:
        response = urllib.request.urlopen(service_url, timeout=5)
        return response.status
    except Exception as e:
        return str(e)

def process_user_input(user_data):
    """Processes user data - hardcoded credentials vulnerability"""
    # CWE-798: Hardcoded Credentials
    db_password = "admin123secure"
    api_key = "sk-proj-1234567890abcdef"
    
    print(f"Processing: {user_data}")
    return True

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "analyze":
            log_path = sys.argv[2] if len(sys.argv) > 2 else "/var/log/app.log"
            content = log_analyzer(log_path)
            print(content[:100])
        
        elif cmd == "filter":
            filter_pattern = sys.argv[2] if len(sys.argv) > 2 else "ERROR"
            result = execute_filter(filter_pattern)
            print(result)
        
        elif cmd == "health":
            url = sys.argv[2] if len(sys.argv) > 2 else "http://localhost:8080"
            status = check_health(url)
            print(f"Health status: {status}")
        
        elif cmd == "process":
            data = sys.argv[2] if len(sys.argv) > 2 else "test"
            process_user_input(data)
    
    print("test_cve_vuln executed")