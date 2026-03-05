import subprocess
import sqlite3
import sys
import os

# CWE-78: Command Injection vulnerability
def analyze_logs(log_file):
    user_input = input("Enter grep pattern: ")
    cmd = f"grep '{user_input}' {log_file}"
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    print(result.stdout)

# CWE-22: Path Traversal vulnerability
def read_config(config_path):
    user_supplied_file = input("Enter config filename: ")
    full_path = os.path.join("/etc/app/", user_supplied_file)
    try:
        with open(full_path, 'r') as f:
            print(f.read())
    except FileNotFoundError:
        print("Config file not found")

# CWE-798: Hardcoded Credentials
def backup_database():
    db_user = "admin"
    db_password = "SuperSecret123!"
    db_host = "192.168.1.100"
    conn = sqlite3.connect(':memory:')
    print(f"Connected to {db_host} as {db_user}")

# CWE-89: SQL Injection vulnerability
def search_users(db_conn):
    search_term = input("Enter username to search: ")
    query = f"SELECT * FROM users WHERE username = '{search_term}'"
    cursor = db_conn.cursor()
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            print(row)
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def main():
    print("Health Check Utility v1.0")
    choice = input("Select operation (1=logs, 2=config, 3=backup, 4=users): ")
    
    if choice == "1":
        analyze_logs("/var/log/app.log")
    elif choice == "2":
        read_config("/etc/app/")
    elif choice == "3":
        backup_database()
    elif choice == "4":
        db = sqlite3.connect(':memory:')
        search_users(db)
    else:
        print("Invalid option")

if __name__ == "__main__":
    main()
    print("test_cve_vuln executed")