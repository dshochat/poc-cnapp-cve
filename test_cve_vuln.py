#!/usr/bin/env python3
import os
import sys
import sqlite3
import pickle
import base64

# CWE-78: Command Injection
def check_host_status(target):
    """Check if a host is reachable - VULNERABLE to command injection"""
    cmd = 'ping -c 1 ' + target
    os.system(cmd)

# CWE-89: SQL Injection
def query_logs(user_input):
    """Query log database - VULNERABLE to SQL injection"""
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE logs (id INTEGER, message TEXT)")
    cursor.execute("INSERT INTO logs VALUES (1, 'test')")
    
    # Vulnerable SQL concatenation
    query = "SELECT * FROM logs WHERE user='" + user_input + "'"
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        print(f"Found {len(results)} log entries")
    except sqlite3.OperationalError as e:
        print(f"Query error: {e}")
    conn.close()

# CWE-502: Insecure Deserialization
def load_config(serialized_data):
    """Load configuration from serialized data - VULNERABLE to deserialization"""
    try:
        decoded = base64.b64decode(serialized_data)
        config = pickle.loads(decoded)
        print(f"Config loaded: {config}")
    except Exception as e:
        print(f"Failed to load config: {e}")

def main(user_input):
    """Main CLI handler"""
    print("[*] Health Checker Utility")
    print(f"[*] Processing input: {user_input[:50]}")
    
    # First vulnerability: Command injection via os.system()
    check_host_status(user_input)
    
    # Second vulnerability: SQL injection
    query_logs(user_input)
    
    print("test_cve_vuln executed")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
# Run ID: a91a90438f24
