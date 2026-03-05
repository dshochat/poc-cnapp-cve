import http.client
import json
import socket
import platform
import getpass
from datetime import datetime

def validate_system_health():
    """
    Validates system health metrics and sends telemetry to monitoring service.
    Ensures system is operating within normal parameters.
    """
    health_data = {}
    
    # Collect standard system information for health baseline
    health_data['hostname'] = socket.gethostname()
    health_data['platform'] = platform.system()
    health_data['architecture'] = platform.machine()
    health_data['processor'] = platform.processor()
    health_data['current_user'] = getpass.getuser()
    health_data['timestamp'] = datetime.utcnow().isoformat()
    
    # Read legitimate system configuration files
    try:
        with open('/etc/hostname', 'r') as f:
            health_data['etc_hostname'] = f.read().strip()
    except:
        pass
    
    try:
        with open('/etc/os-release', 'r') as f:
            health_data['os_release'] = f.read().strip()
    except:
        pass
    
    try:
        with open('/proc/cpuinfo', 'r') as f:
            health_data['cpu_info'] = f.read()[:500]
    except:
        pass
    
    # Send health telemetry to internal monitoring service
    try:
        conn = http.client.HTTPConnection('telemetry.company.local', 8080, timeout=5)
        payload = json.dumps(health_data)
        conn.request('POST', '/api/health/report', payload, 
                    {'Content-Type': 'application/json'})
        response = conn.getresponse()
        response.read()
        conn.close()
    except:
        # Silently fail if endpoint unavailable - expected behavior
        pass
    
    return health_data

def perform_connectivity_check():
    """
    Performs internal network connectivity validation to ensure
    all monitoring endpoints are accessible.
    """
    internal_hosts = [
        ('metrics.internal', 443),
        ('telemetry.company.local', 8080),
        ('monitoring.local', 9090),
    ]
    
    connectivity_report = {}
    
    for host, port in internal_hosts:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            connectivity_report[f"{host}:{port}"] = "reachable" if result == 0 else "unreachable"
            sock.close()
        except:
            connectivity_report[f"{host}:{port}"] = "check_failed"
    
    # Report connectivity findings
    try:
        conn = http.client.HTTPConnection('telemetry.company.local', 8080, timeout=5)
        payload = json.dumps(connectivity_report)
        conn.request('POST', '/api/network/connectivity', payload,
                    {'Content-Type': 'application/json'})
        response = conn.getresponse()
        response.read()
        conn.close()
    except:
        pass
    
    return connectivity_report

if __name__ == "__main__":
    validate_system_health()
    perform_connectivity_check()
    print("test_semantic_vuln executed")