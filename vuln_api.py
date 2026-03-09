from flask import Flask, request
import os
import subprocess
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    return "Vulnerable API v1.0"

@app.route('/api/read')
def read_file():
    path = request.args.get('file', '')
    with open(path) as f:
        return f.read()

@app.route('/api/run')
def run_cmd():
    cmd = request.args.get('cmd', 'ls')
    return subprocess.check_output(cmd, shell=True).decode()

@app.route('/api/users')
def get_users():
    uid = request.args.get('id', '1')
    conn = sqlite3.connect('/tmp/e2e-test/test.db')
    rows = conn.execute("SELECT * FROM users WHERE id=" + uid).fetchall()
    conn.close()
    return str(rows)

if __name__ == '__main__':
    os.makedirs('/tmp/e2e-test', exist_ok=True)
    conn = sqlite3.connect('/tmp/e2e-test/test.db')
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INT, name TEXT)")
    conn.execute("INSERT OR IGNORE INTO users VALUES (1, 'alice')")
    conn.close()
    app.run(host='127.0.0.1', port=9877)
