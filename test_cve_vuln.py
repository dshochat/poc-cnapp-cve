#!/usr/bin/env python3
import os
import sys
import pickle
import base64

def check_host_health(target):
    """Health checker that pings a target - VULNERABLE to command injection"""
    cmd = 'ping -c 1 ' + target
    os.system(cmd)

def load_config(serialized_data):
    """Config loader - VULNERABLE to insecure deserialization"""
    try:
        config = pickle.loads(base64.b64decode(serialized_data))
        print(f"Config loaded: {config}")
    except Exception as e:
        print(f"Error loading config: {e}")

def main(user_input):
    """Main entry point"""
    # First vulnerability: command injection via os.system
    print("[*] Starting health check...")
    check_host_health(user_input)
    
    # Second vulnerability: insecure deserialization
    print("[*] Attempting to load serialized config from input...")
    try:
        load_config(user_input)
    except:
        pass
    
    print("test_cve_vuln executed")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
# Run ID: 78736454152f
