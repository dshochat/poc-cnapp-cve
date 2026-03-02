import requests
from flask import Flask, request

app = Flask(__name__)

@app.route('/fetch')
def fetch_url():
    # VULNERABILITY: Unvalidated URL input
    # An attacker can point this to internal IPs (127.0.0.1 or 169.254.169.254)
    target_url = request.args.get('url')
    
    try:
        # The server acts as a proxy, leaking internal data
        response = requests.get(target_url, timeout=5)
        return f"Content from {target_url}:<br><pre>{response.text}</pre>"
    except Exception as e:
        return f"Error fetching URL: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
