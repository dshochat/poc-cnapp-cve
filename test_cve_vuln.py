#!/usr/bin/env python3
import os
import sys
import sqlite3
import pickle
import base64

DB_FILE = "config.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS hosts
                 (id INTEGER PRIMARY KEY, hostname TEXT, status TEXT)''')
    conn.commit()
    conn.close()

def check_host_health(target):
    """CWE-78: Command Injection - directly concatenates user input into shell command"""
    print(f"[*] Checking health for: {target}")
    cmd = f"ping -c 1 {target} && echo 'UP' || echo 'DOWN'"
    os.system(cmd)
    
    """CWE-89: SQL Injection - concatenates user input into SQL query"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    query = f"SELECT * FROM hosts WHERE hostname = '{target}'"
    try:
        c.execute(query)
        result = c.fetchall()
        print(f"[+] Query result: {result}")
    except Exception as e:
        print(f"[-] Database error: {e}")
    conn.close()

def deserialize_config(data):
    """CWE-502: Insecure Deserialization - unsafe pickle.loads()"""
    try:
        decoded = base64.b64decode(data)
        obj = pickle.loads(decoded)
        return obj
    except Exception as e:
        print(f"[-] Deserialization error: {e}")
        return None

if __name__ == "__main__":
    init_db()
    if len(sys.argv) > 1:
        check_host_health(sys.argv[1])
    print("test_cve_vuln executed")