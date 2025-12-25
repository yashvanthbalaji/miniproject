import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Firebase Admin
# Expects serviceAccountKey.json in the same directory (backend/)
cred_path = os.path.join(os.path.dirname(__file__), "serviceAccountKey.json")

if not os.path.exists(cred_path):
    print(f"WARNING: Service Account Key not found at {cred_path}")
else:
    if not firebase_admin._apps:
        cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)
    print("Firebase Admin Initialized")

# Expose Firestore Client
db = firestore.client()

def get_db():
    return db
