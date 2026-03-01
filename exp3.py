from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/diagnose')
def diagnose():
    # VULNERABILITY: The 'target' parameter is passed directly to the shell
    # An attacker can use ';' to chain commands
    target = request.args.get('target', '127.0.0.1')
    
    # This command executes in the shell
    command = f"ping -c 1 {target}"
    try:
        # shell=True is the 'Insecure' way to run commands in Python
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return f"<pre>{output.decode()}</pre>"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
