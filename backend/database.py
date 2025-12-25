import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

# Initialize Firebase Admin
if not firebase_admin._apps:
    firebase_creds = os.getenv("FIREBASE_CREDENTIALS")
    
    if firebase_creds:
        # Production/Render: Use environment variable
        print("Initializing Firebase from Environment Variable")
        cred_dict = json.loads(firebase_creds)
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    else:
        # Local Development: Use file
        cred_path = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")
        if os.path.exists(cred_path):
            print(f"Initializing Firebase from File: {cred_path}")
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        else:
            print("WARNING: No Firebase credentials found (checked Env Var and File)")

# Expose Firestore Client
# Only create client if app is initialized to avoid errors
try:
    db = firestore.client()
except Exception as e:
    print(f"Error creating Firestore client: {e}")
    db = None

def get_db():
    return db
