import pickle
import base64

@app.route('/load_profile')
def load_profile():
    # EXPLOIT: Insecure Deserialization (RCE)
    # The 'data' param is base64 encoded pickled data from the user
    user_data = request.args.get('data')
    if user_data:
        try:
            # Dangerous: pickle.loads executes code embedded in the data
            decoded_data = base64.b64decode(user_data)
            profile = pickle.loads(decoded_data)
            return f"Welcome back, {profile.get('name', 'User')}!"
        except Exception as e:
            return f"Error loading profile: {str(e)}"
    return "No profile data provided."
