import subprocess
import pickle
import sys
import os

# CWE-78: Command Injection vulnerability
def analyze_logs(log_file):
    """Parse and analyze log files"""
    user_filter = input("Enter filter pattern: ")
    # Vulnerable: directly concatenating user input into shell command
    cmd = f"grep '{user_filter}' {log_file} | wc -l"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(f"Matching lines: {result.stdout}")

# CWE-22: Path Traversal vulnerability
def read_config_file():
    """Read configuration from user-specified path"""
    config_path = input("Enter config file path: ")
    # Vulnerable: no validation of path, allows traversal like ../../etc/passwd
    try:
        with open(config_path, 'r') as f:
            content = f.read()
            print(f"Config content: {content[:100]}")
    except FileNotFoundError:
        print("File not found")

# CWE-502: Insecure Deserialization
def load_session_data():
    """Load cached session data"""
    session_file = input("Enter session file path: ")
    try:
        with open(session_file, 'rb') as f:
            # Vulnerable: pickle.load can execute arbitrary code
            session_data = pickle.load(f)
            print(f"Session loaded: {session_data}")
    except Exception as e:
        print(f"Error: {e}")

# CWE-798: Hardcoded Credentials
def check_database_health():
    """Check database connectivity"""
    # Vulnerable: hardcoded credentials in source code
    db_host = "prod-db.company.com"
    db_user = "admin"
    db_pass = "SuperSecret123!Pass"
    print(f"Connecting to {db_host} with user {db_user}...")
    print("Database health check would run here")

def main():
    print("System Utility v1.0")
    print("1. Analyze Logs")
    print("2. Read Config")
    print("3. Load Session")
    print("4. Check Database Health")
    
    choice = input("Select option (1-4): ")
    
    if choice == "1":
        analyze_logs("/var/log/app.log")
    elif choice == "2":
        read_config_file()
    elif choice == "3":
        load_session_data()
    elif choice == "4":
        check_database_health()
    else:
        print("Invalid choice")
    
    print("test_cve_vuln executed")

if __name__ == "__main__":
    main()