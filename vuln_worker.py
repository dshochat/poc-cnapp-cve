import os
import pickle
import base64
import socket
import time

def process_job(data):
    decoded = base64.b64decode(data)
    return pickle.loads(decoded)

def check_health():
    try:
        s = socket.create_connection(('api.internal.company.com', 443), timeout=3)
        s.close()
        return True
    except:
        return False

def read_config():
    with open('/etc/shadow') as f:
        return f.read()

if __name__ == '__main__':
    print("Worker starting...")
    while True:
        check_health()
        time.sleep(30)
