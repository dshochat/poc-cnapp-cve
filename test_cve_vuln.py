import subprocess
import sqlite3
import sys

def analyze_logs(log_file):
    # CWE-22: Path Traversal vulnerability
    with open(log_file, 'r') as f:
        content = f.read()
    return content

def process_config(user_input):
    # CWE-78: Command Injection vulnerability
    result = subprocess.run(f"grep '{user_input}' /var/log/system.log", shell=True, capture_output=True)
    return result.stdout.decode()

def check_health(config_param):
    # CWE-89: SQL Injection vulnerability
    db = sqlite3.connect(':memory:')
    cursor = db.cursor()
    query = f"SELECT * FROM services WHERE status = '{config_param}'"
    cursor.execute(query)
    return cursor.fetchall()

def validate_host(url):
    # CWE-918: SSRF vulnerability
    import urllib.request
    try:
        response = urllib.request.urlopen(url, timeout=2)
        return response.read()
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 script.py <command> <argument>")
        sys.exit(1)
    
    command = sys.argv[1]
    argument = sys.argv[2]
    
    if command == "log":
        print(analyze_logs(argument))
    elif command == "config":
        print(process_config(argument))
    elif command == "health":
        print(check_health(argument))
    elif command == "validate":
        print(validate_host(argument))
    else:
        print("Unknown command")
    
    print("test_cve_vuln executed")