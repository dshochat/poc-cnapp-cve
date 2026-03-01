from flask import Flask, request
import pickle
import base64
import os

app = Flask(__name__)

@app.route('/load_profile')
def load_profile():
    user_data = request.args.get('data')
    if user_data:
        try:
            decoded_data = base64.b64decode(user_data)
            # This is the "Echo" point the sensor will watch
            profile = pickle.loads(decoded_data)
            return f"Welcome back, {profile.get('name', 'User')}!"
        except Exception as e:
            return f"Error: {str(e)}"
    return "No profile data provided."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001) # Use a different port if 5000 is busy
