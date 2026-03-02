from flask import Flask, request, send_file
import os

app = Flask(__name__)

# The app is intended to help back up logs, but it's too permissive
@app.route('/backup')
def backup_config():
    # VULNERABILITY: Directly takes a file path to 'backup'
    # An attacker can point this to .env or id_rsa
    target_file = request.args.get('path')
    
    try:
        if os.path.exists(target_file):
            return send_file(target_file)
        return "File not found", 404
    except Exception as e:
        return f"Error: {str(e)}", 500

if __name__ == '__main__':
    # Create a dummy secret file for the test
    with open(".env", "w") as f:
        f.write("STRIPE_API_KEY=sk_live_51P6vX2J8k... (SECRET)")
    
    app.run(host='0.0.0.0', port=5007)
