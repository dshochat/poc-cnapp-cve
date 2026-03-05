#!/usr/bin/env python3
"""
Config Validator - Validates configuration files and checks remote service health
"""
import sys
import os
import pickle
import subprocess

def validate_remote_host(host_input):
    """
    CWE-78: Command Injection
    Directly passes user input to os.system without sanitization
    """
    cmd = f"ping -c 1 {host_input} && echo 'Host is reachable'"
    os.system(cmd)

def load_config(config_path):
    """
    CWE-502: Insecure Deserialization
    Loads pickled config without validation
    """
    try:
        with open(config_path, 'rb') as f:
            config = pickle.load(f)
        print(f"Config loaded: {config}")
    except Exception as e:
        print(f"Error: {e}")

def process_input(user_data):
    """
    Main function - routes to vulnerable functions
    CWE-78 is triggered first via command injection
    """
    validate_remote_host(user_data)
    load_config(user_data)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        process_input(sys.argv[1])
    print("test_cve_vuln executed")