import sys
import os
from unittest.mock import MagicMock, patch

# Add current directory to path
sys.path.append(os.getcwd())

# Mock necessary dependencies BEFORE importing main
# We need to mock joblib to avoid loading actual models if they are heavy or missing
with patch('joblib.load') as mock_load:
    # Import the module under test
    from backend import main

def test_email_notifications():
    print("=== Verifying Email Notifications ===")

    # 1. Setup Mocks
    # Mock the models in main.models
    mock_model_uci = MagicMock()
    mock_model_uci.predict_proba.return_value = [[0.1, 0.8]] # 80% risk
    main.models["uci"] = mock_model_uci

    mock_model_lifestyle = MagicMock()
    mock_model_lifestyle.predict_proba.return_value = [[0.9, 0.1]] # 10% risk
    main.models["lifestyle"] = mock_model_lifestyle
    
    # Mock DB and User
    mock_db = MagicMock()
    mock_user = MagicMock()
    mock_user.id = 1
    mock_user.email = "test_user@example.com"

    # Mock send_email to verify calls
    with patch('backend.main.send_email') as mock_send_email:
        
        # 2. Test Acute Prediction
        print("\n[Test] Acute Prediction...")
        acute_input = main.AcuteInput(
            age=50, sex=1, cp=0, trestbps=140, chol=240, fbs=0, 
            restecg=0, thalach=150, exang=0, oldpeak=2.5, slope=1, 
            ca=0, thal=2
        )
        
        try:
            main.predict_acute(acute_input, current_user=mock_user, db=mock_db)
            print("✅ predict_acute executed without error.")
        except Exception as e:
            print(f"❌ predict_acute failed: {e}")

        # Verify email was called
        # Acute risk was 0.8 (80%)
        mock_send_email.assert_called_with("test_user@example.com", 0.8)
        print("✅ Verified: Email sent for Acute Prediction.")
        mock_send_email.reset_mock()

        # 3. Test Lifestyle Prediction
        print("\n[Test] Lifestyle Prediction...")
        lifestyle_input = main.LifestyleInput(
            age=50, gender=1, height=170, weight=70, ap_hi=120, ap_lo=80,
            cholesterol=1, gluc=1, smoke=0, alco=0, active=1
        )

        try:
            main.predict_lifestyle(lifestyle_input, current_user=mock_user, db=mock_db)
            print("✅ predict_lifestyle executed without error.")
        except Exception as e:
            print(f"❌ predict_lifestyle failed: {e}")

        # Verify email was called
        # Lifestyle risk was 0.1 (10%)
        mock_send_email.assert_called_with("test_user@example.com", 0.1)
        print("✅ Verified: Email sent for Lifestyle Prediction.")
        
    print("\n=== Verification Complete ===")

if __name__ == "__main__":
    test_email_notifications()
