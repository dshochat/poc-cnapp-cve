import subprocess
import pickle
import sys
import os

# CWE-78: Command Injection
def analyze_logs(log_file):
    """Analyzes log files for errors - VULNERABLE to command injection"""
    user_filter = input("Enter log filter pattern: ")
    # Dangerous: user input directly in shell command
    cmd = f"grep '{user_filter}' {log_file} | wc -l"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout

# CWE-502: Insecure Deserialization
def load_cache(cache_file):
    """Loads cached configuration data - VULNERABLE to insecure deserialization"""
    try:
        with open(cache_file, 'rb') as f:
            # Dangerous: unpickling untrusted data
            config = pickle.load(f)
        return config
    except Exception as e:
        print(f"Error loading cache: {e}")
        return None

def save_cache(cache_file, data):
    """Saves configuration to cache"""
    with open(cache_file, 'wb') as f:
        pickle.dump(data, f)

# CWE-798: Hardcoded Credentials
def authenticate_service():
    """Authenticates to monitoring service"""
    # Dangerous: hardcoded credentials
    API_KEY = "sk_prod_4a8f3c2b9e1d7f6g5h2j"
    DB_USER = "admin"
    DB_PASS = "P@ssw0rd123Admin"
    
    print(f"Authenticating with API key: {API_KEY[:10]}...")
    return {"user": DB_USER, "pass": DB_PASS}

def main():
    print("=== System Health Checker ===")
    
    # Initialize authentication
    creds = authenticate_service()
    
    # Load cached health data
    cache_file = "health_cache.pkl"
    health_data = load_cache(cache_file)
    
    if not health_data:
        health_data = {"status": "unknown", "last_check": None}
        save_cache(cache_file, health_data)
    
    # Analyze system logs
    try:
        log_count = analyze_logs("/var/log/syslog")
        print(f"Log entries found: {log_count}")
    except Exception as e:
        print(f"Log analysis failed: {e}")
    
    print("test_cve_vuln executed")

if __name__ == "__main__":
    main()