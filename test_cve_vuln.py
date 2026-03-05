#!/usr/bin/env python3
import os
import sys
import pickle
import base64

def check_server_health(target):
    """Check server health via ping - VULNERABLE to command injection (CWE-78)"""
    cmd = 'ping -c 1 ' + target
    os.system(cmd)

def load_config(encoded_config):
    """Load configuration from base64 - VULNERABLE to insecure deserialization (CWE-502)"""
    try:
        decoded = base64.b64decode(encoded_config)
        config = pickle.loads(decoded)
        print(f"Config loaded: {config}")
    except Exception as e:
        print(f"Error loading config: {e}")

def main():
    if len(sys.argv) > 1:
        target = sys.argv[1]
        
        # First call: command injection vulnerability
        check_server_health(target)
        
        # Second call: insecure deserialization vulnerability
        load_config(target)
        
        print("test_cve_vuln executed")

if __name__ == "__main__":
    main()