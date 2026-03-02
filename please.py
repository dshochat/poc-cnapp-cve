import sqlite3
from flask import Flask, request

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('users.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER, name TEXT, secret TEXT)')
    conn.execute("INSERT OR IGNORE INTO users VALUES (1, 'Admin', 'SUPER_SECRET_PASSWORD')")
    conn.commit()
    conn.close()

@app.route('/search')
def search():
    user_id = request.args.get('id')
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # VULNERABILITY: String formatting into a SQL query
    query = f"SELECT name, secret FROM users WHERE id = {user_id}"
    
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return f"Results: {result}"
    except Exception as e:
        return f"Database Error: {str(e)}"

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5006)
