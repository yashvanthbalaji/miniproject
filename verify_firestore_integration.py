import sys
import os
import json
import time

# Add current directory to path
sys.path.append(os.getcwd())

# Ensure we can import backend
try:
    from backend.database import get_db
    from backend.main import predict_acute, AcuteInput
    from backend.profile_routes import create_or_update_profile, ProfileBase
except ImportError as e:
    print(f"Import Error: {e}")
    sys.exit(1)

def verify_firestore():
    print("=== Verifying Firestore Integration ===")
    
    # Use a specific test UID
    TEST_UID = "test_script_user_v1"
    TEST_EMAIL = "test_script@example.com"
    
    # Mock Token (Since we call functions directly, we bypass FastAPI Depends)
    mock_token = {
        "uid": TEST_UID,
        "email": TEST_EMAIL
    }
    
    # Mock Models to avoid 503 error
    from unittest.mock import MagicMock
    import backend.main as main_app
    
    mock_uci = MagicMock()
    mock_uci.predict_proba.return_value = [[0.1, 0.9]] # 90% risk
    main_app.models["uci"] = mock_uci
    
    db = get_db()
    
    # 1. Test Profile Creation
    print("\n[1] Testing Profile Save...")
    profile_data = ProfileBase(
        age=30, gender="Male", height=180, weight=75,
        stress_level=3, glucose=1, smoke=0, alco=0, active=1
    )
    
    try:
        # Call the route handler directly
        res = create_or_update_profile(profile_data, token=mock_token)
        print("✅ Profile function returned success.")
        
        # Verify in Firestore
        doc = db.collection('users').document(TEST_UID).collection('data').document('profile').get()
        if doc.exists:
            print("✅ Verified: Profile document exists in Firestore.")
            print(f"   Data: {doc.to_dict()}")
        else:
            print("❌ Verified: Profile document NOT found.")
    except Exception as e:
        print(f"❌ Profile Test Failed: {e}")
        import traceback
        traceback.print_exc()

    # 2. Test Prediction History
    print("\n[2] Testing Acute Prediction Log...")
    acute_input = AcuteInput(
        age=30, sex=1, cp=0, trestbps=120, chol=200, fbs=0, 
        restecg=0, thalach=150, exang=0, oldpeak=0, slope=1, 
        ca=0, thal=2
    )
    
    try:
        # Mock Email sending to avoid spamming or crashing if no credential
        # We assume email logic works as tested previously, focus here is Firestore
        res = predict_acute(acute_input, token=mock_token)
        print("✅ Prediction function returned success.")
        
        # Verify in Firestore
        # Give it a moment? Firestore is usually fast locally/direct
        preds = db.collection('users').document(TEST_UID).collection('predictions').order_by('timestamp', direction='DESCENDING').limit(1).stream()
        found = False
        for p in preds:
            found = True
            data = p.to_dict()
            print("✅ Verified: Prediction document found in Firestore.")
            print(f"   Risk: {data.get('risk_probability')}, Label: {data.get('risk_label')}")
            break
        
        if not found:
            print("❌ Verified: Prediction document NOT found.")
            
    except Exception as e:
        print(f"❌ Prediction Test Failed: {e}")
        import traceback
        traceback.print_exc()

    print("\n=== Verification Complete ===")

if __name__ == "__main__":
    verify_firestore()
