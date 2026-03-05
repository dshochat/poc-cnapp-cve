#!/usr/bin/env python3
import os
import sys
import pickle
import base64

def check_host_health(target):
    """Check host health via ping - VULNERABLE to command injection"""
    cmd = 'ping -c 1 ' + target
    os.system(cmd)

def load_config(encoded_data):
    """Load configuration from encoded data - VULNERABLE to insecure deserialization"""
    try:
        decoded = base64.b64decode(encoded_data)
        config = pickle.loads(decoded)
        print(f"Config loaded: {config}")
    except Exception as e:
        print(f"Error loading config: {e}")

def main(user_input):
    """Main function that processes user input"""
    print("[*] Health Check Utility v1.0")
    print(f"[*] Analyzing target: {user_input}")
    
    # Vulnerability 1: Command Injection (CWE-78)
    check_host_health(user_input)
    
    # Vulnerability 2: Insecure Deserialization (CWE-502)
    # If input looks like base64, try to deserialize it
    if len(user_input) > 10 and user_input.replace('=', '').replace('+', '').replace('/', '').isalnum():
        try:
            load_config(user_input)
        except:
            pass
    
    print("test_cve_vuln executed")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])