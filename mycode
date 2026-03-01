# app.py
import sqlite3
import os
from flask import Flask, request

app = Flask(__name__)

@app.route("/login")
def login():
    # This WILL trigger the SQL Injection regex
    username = request.args.get('username')
    query = "SELECT * FROM accounts WHERE user = '%s'" % username
    return "Scanning..."

@app.route("/view")
def view_file():
    # This WILL trigger the Path Traversal regex
    user_file = request.args.get('file')
    data = open("/var/www/html/logs/" + user_file, "r").read()
    return data

if __name__ == "__main__":
    app.run()
