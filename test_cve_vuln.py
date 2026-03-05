import sys
import os
import sqlite3
import subprocess

def log_analyzer(log_file):
    # CWE-22: Path Traversal
    with open(log_file, 'r') as f:
        return f.read()

def process_command(user_input):
    # CWE-78: Command Injection
    result = os.system('echo "Processing: ' + user_input + '"')
    return result

def check_host(hostname):
    # CWE-78: Command Injection via ping
    cmd = 'ping -c 1 ' + hostname
    subprocess.call(cmd, shell=True)

def get_config_value(config_key):
    # CWE-89: SQL Injection
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE config (key TEXT, value TEXT)")
    cursor.execute("INSERT INTO config VALUES ('db_host', 'localhost')")
    cursor.execute("INSERT INTO config VALUES ('db_user', 'admin')")
    
    query = "SELECT value FROM config WHERE key = '" + config_key + "'"
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 script.py <mode> <input>")
        print("Modes: analyze, process, ping, config")
        sys.exit(1)
    
    mode = sys.argv[1]
    user_data = sys.argv[2]
    
    if mode == "analyze":
        try:
            content = log_analyzer(user_data)
            print(content[:100])
        except Exception as e:
            print(f"Error: {e}")
    
    elif mode == "process":
        process_command(user_data)
    
    elif mode == "ping":
        check_host(user_data)
    
    elif mode == "config":
        result = get_config_value(user_data)
        print(f"Config value: {result}")
    
    print("test_cve_vuln executed")