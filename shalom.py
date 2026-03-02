import os
from flask import Flask, request, render_template_string

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']
    # VULNERABILITY: Using the filename directly from the user without sanitization
    # An attacker can use '../' to traverse directories
    filename = file.filename
    
    # Path Traversal: This could resolve to /home/test/app/uploads/../../.bashrc
    save_path = os.path.join(UPLOAD_FOLDER, filename)
    
    try:
        file.save(save_path)
        return f"File saved to: {save_path}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
