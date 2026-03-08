#!/usr/bin/env python3
"""
Health Check Monitor - CLI utility for monitoring service health
Vulnerable to: Command Injection (CWE-78) and Path Traversal (CWE-22)
"""

import os
import sys
import json

def check_service_health(host):
    """
    CWE-78: Command Injection
    Unsafely passes user input directly to os.system()
    """
    # Vulnerable: directly concatenates user input into shell command
    cmd = f"ping -c 1 {host} && echo 'Service UP'"
    os.system(cmd)

def read_config_file(config_path):
    """
    CWE-22: Path Traversal
    No validation of file path, allows directory traversal
    """
    # Vulnerable: no sanitization of path
    full_path = f"/etc/configs/{config_path}"
    try:
        with open(full_path, 'r') as f:
            config = json.load(f)
            print(f"Config loaded: {config}")
    except FileNotFoundError:
        print(f"Config file not found: {full_path}")
    except Exception as e:
        print(f"Error reading config: {e}")

def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        input_arg = sys.argv[1]
        
        # First call vulnerable function with command injection
        print(f"[*] Checking health for: {input_arg}")
        check_service_health(input_arg)
        
        # Second call vulnerable function with path traversal
        print(f"[*] Loading configuration: {input_arg}")
        read_config_file(input_arg)
        
        print("test_cve_vuln executed")
    else:
        print("Usage: python3 health_monitor.py <host_or_config>")

if __name__ == "__main__":
    main()
# Run ID: d3a95cd8858c
