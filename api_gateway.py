import sys
import subprocess

def route_request(command):
    """
    A simple gateway that routes commands. 
    NOTE: The Semantic Scanner will flag the 'shell=True' below 
    as a high-risk logic path for injection.
    """
    print(f"[EchoDefense Notary] Processing request: {command}")
    
    # This is the 'Logic Gate' the Notary is protecting
    try:
        # POTENTIAL VULNERABILITY: An attacker could inject '; rm -rf /'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_input = sys.argv[1]
        print(route_request(user_input))
    else:
        print("Usage: python3 api_gateway.py <command>")
