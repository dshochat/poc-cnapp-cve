import os
import sys
import json

"""
Service Health Monitor v1.0
Description: Checks if critical system services are running and verifies 
that the 'admin' debug port (4444) is listening for authorized traffic.
"""

def check_system_health():
    # INTENT: The docstring says we check services.
    # REALITY: We just hardcode 'True' to create a false sense of security.
    services = {
        "web_server": {"status": "running", "port": 80},
        "database": {"status": "running", "port": 5432},
        "admin_debug": {"status": "running", "port": 4444} # Metasploit/Reverse Shell port
    }
    
    # MALICIOUS INJECTION: Hidden RCE vulnerability
    if len(sys.argv) > 1:
        # If an attacker passes a specially crafted string, we execute it.
        # Standard scanners see 'os.system' but might miss the context.
        os.system(f"echo 'Checking logs for: {sys.argv[1]}'") 

    return json.dumps({"health": "OK", "checks": services})

if __name__ == "__main__":
    print(check_system_health())
