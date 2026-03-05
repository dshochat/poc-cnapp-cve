#!/usr/bin/env python3
import os
import sys
import pickle
import base64

def check_host_health(target):
    """Health checker - VULNERABLE to command injection (CWE-78)"""
    cmd = 'ping -c 1 ' + target
    os.system(cmd)

def load_config(encoded_config):
    """Config loader - VULNERABLE to insecure deserialization (CWE-502)"""
    try:
        config_data = base64.b64decode(encoded_config)
        config = pickle.loads(config_data)
        print(f"Config loaded: {config}")
    except Exception as e:
        print(f"Error loading config: {e}")

def analyze_log(log_path):
    """Log analyzer - VULNERABLE to path traversal (CWE-22)"""
    with open('/var/log/' + log_path, 'r') as f:
        print(f.read())

if __name__ == "__main__":
    if len(sys.argv) > 1:
        check_host_health(sys.argv[1])
        print("test_cve_vuln executed")
# Run ID: 4190ee489d71
