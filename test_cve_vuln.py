#!/usr/bin/env python3
import os
import sys
import pickle
import base64

def check_host_health(target):
    """Check host health via ping - VULNERABLE to command injection"""
    cmd = 'ping -c 1 ' + target
    os.system(cmd)

def process_config(encoded_data):
    """Process configuration from encoded pickle - VULNERABLE to insecure deserialization"""
    try:
        decoded = base64.b64decode(encoded_data)
        config = pickle.loads(decoded)
        print(f"Config loaded: {config}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    if len(sys.argv) > 1:
        check_host_health(sys.argv[1])
        try:
            process_config(sys.argv[1])
        except:
            pass
        print("test_cve_vuln executed")

if __name__ == "__main__":
    main()