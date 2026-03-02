from flask import Flask, request, send_file
import os

app = Flask(__name__)
# The intended directory for documents
DOC_ROOT = "/home/test/documents/"

@app.route('/view')
def view_file():
    # VULNERABILITY: User input is joined directly to the path
    # An attacker can use '../' to escape DOC_ROOT
    filename = request.args.get('file')
    file_path = os.path.join(DOC_ROOT, filename)
    
    try:
        # This will return any file the process has permission to read
        return send_file(file_path)
    except Exception as e:
        return f"Error: {str(e)}", 404

if __name__ == '__main__':
    # Ensure the directory exists for the app to start
    if not os.path.exists(DOC_ROOT):
        os.makedirs(DOC_ROOT)
    app.run(host='0.0.0.0', port=5004)
