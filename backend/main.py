from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
import pandas as pd
import joblib
import os
import json
import datetime
from fastapi.middleware.cors import CORSMiddleware
from .auth import routes as auth_routes
from . import profile_routes
from .database import get_db
from .auth.routes import verify_firebase_token

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(profile_routes.router)

# Load Model Pipeline (includes preprocessor + model)
model_pipeline = None

# Load Model Pipelines
models = {
    "uci": None,
    "lifestyle": None,
    "synthetic": None
}

@app.on_event("startup")
def load_artifacts():
    global models
    import traceback
    try:
        models["uci"] = joblib.load('model_uci.pkl')
        print("Model UCI loaded.")
    except Exception as e:
        print(f"FATAL: Model UCI failed to load: {e}")
        traceback.print_exc()
    
    try:
        models["lifestyle"] = joblib.load('model_lifestyle.pkl')
        print("Model Lifestyle loaded.")
    except Exception as e:
        print(f"FATAL: Model Lifestyle failed to load: {e}")
        traceback.print_exc()
    
    try:
        models["synthetic"] = joblib.load('model_synthetic.pkl')
        print("Model Synthetic loaded.")
    except Exception as e:
        print(f"FATAL: Model Synthetic failed to load: {e}")
        traceback.print_exc()

# Input Schemas
class AcuteInput(BaseModel):
    age: int
    sex: int
    cp: int
    trestbps: int
    chol: int
    fbs: int
    restecg: int
    thalach: int
    exang: int
    oldpeak: float
    slope: int
    ca: int
    thal: int
    phone_number: str = None

class LifestyleInput(BaseModel):
    # Only fields not in Profile or overrideable
    # Ideally frontend sends everything merged
    age: int
    gender: int
    height: float
    weight: float
    ap_hi: int
    ap_lo: int
    cholesterol: int
    gluc: int
    smoke: int
    alco: int
    active: int
    phone_number: str = None

class SyntheticInput(BaseModel):
    stress_level: int
    sleep_hours: float
    daily_steps: int
    water_intake: float
    hrv: int
    age: int
    bmi: float

# Email Config
GMAIL_USER = os.getenv("GMAIL_USER", "cardiacattackpredictor@gmail.com")
GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD", "dbmw subf oqjg rggn")

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email, risk_prob):
    if not to_email:
        print("No email provided for notification.")
        return

    risk_percentage = risk_prob * 100
    
    if risk_percentage < 40:
        subject = "Cardiac Health Status – Low Risk"
        body = (
            f"Result: Low Risk ({risk_percentage:.1f}%)\n\n"
            "We are pleased to inform you that no immediate cardiac concern is detected based on your provided data. "
            "We encourage you to maintain a healthy diet and lifestyle to keep your heart strong.\n\n"
            "Disclaimer: This system provides risk awareness and guidance only and is intended for academic demonstration, not medical diagnosis."
        )
    elif 40 <= risk_percentage <= 70:
        subject = "Cardiac Health Status – Moderate Risk"
        body = (
            f"Result: Moderate Risk ({risk_percentage:.1f}%)\n\n"
            "Your analysis indicates a moderate risk. We advise you to monitor your health parameters closely, "
            "improve lifestyle habits (diet, exercise, stress management), and consider a medical consultation if any symptoms occur.\n\n"
            "Disclaimer: This system provides risk awareness and guidance only and is intended for academic demonstration, not medical diagnosis."
        )
    else: # risk > 70
        subject = "Cardiac Risk Alert – High Risk Detected"
        body = (
            f"Result: High Risk ({risk_percentage:.1f}%)\n\n"
            "ALERT: Your analysis indicates an elevated cardiac risk. We strongly recommend an immediate medical consultation "
            "for a professional assessment.\n\n"
            "Disclaimer: This system provides risk awareness and guidance only and is intended for academic demonstration, not medical diagnosis."
        )

    try:
        # If credentials are mocks, just log it
        if GMAIL_USER == "your_email@gmail.com" or GMAIL_PASSWORD == "your_app_password":
            print(f"[MOCK EMAIL] To: {to_email}\nSubject: {subject}\nBody: {body}\n")
            return

        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(GMAIL_USER, to_email, text)
        server.quit()
        print(f"Email sent to {to_email}")
    except Exception as e:
        print(f"Email Failed: {e}")

@app.get("/debug-email")
def debug_email(to_email: str):
    """
    Temporary endpoint to test email sending and see errors directly.
    Usage: https://your-url.onrender.com/debug-email?to_email=you@example.com
    """
    try:
        # Check if creds are loaded
        if not GMAIL_USER or "your_email" in GMAIL_USER:
            return {"status": "error", "message": "GMAIL_USER not configured properly in Env Vars"}
            
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.set_debuglevel(1) # Enable verbose debug output
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        
        msg = MIMEText("This is a test email from your Cardiac Prediction App.")
        msg['Subject'] = "Test Email - Configuration Success"
        msg['From'] = GMAIL_USER
        msg['To'] = to_email
        
        server.sendmail(GMAIL_USER, to_email, msg.as_string())
        server.quit()
        
        return {"status": "success", "message": f"Email sent successfully to {to_email} from {GMAIL_USER}"}
    except Exception as e:
        return {"status": "error", "message": str(e), "type": type(e).__name__}

def save_history(uid, data, prob, label, m_type):
    try:
        db = get_db()
        timestamp = datetime.datetime.utcnow().isoformat()
        
        doc_data = {
            "timestamp": timestamp,
            "model_type": m_type,
            "input_data": json.dumps(data),
            "risk_probability": prob,
            "risk_label": label
        }
        
        # Save to users/{uid}/predictions (auto-id)
        db.collection("users").document(uid).collection("predictions").add(doc_data)
        
    except Exception as e: print(f"History Save Error: {e}")

# --- Endpoints ---

def get_risk_message(prob):
    p = prob * 100
    if p == 0: return "No immediate cardiac risk detected based on current input."
    if 0 < p <= 20: return "Low cardiac risk. Maintain a healthy lifestyle."
    if 20 < p <= 50: return "Moderate cardiac risk. Lifestyle changes and monitoring recommended."
    if 50 < p <= 80: return "High cardiac risk. Medical consultation advised."
    if 80 < p < 100: return "Very high cardiac risk. Seek medical attention soon."
    if p >= 100: return "Extremely high cardiac risk detected. Please visit the nearest hospital immediately."
    return "Unknown risk level." # Fallback

@app.post("/predict") # Keep legacy endpoint mapping to Acute
@app.post("/predict/acute")
def predict_acute(data: AcuteInput, background_tasks: BackgroundTasks, token: dict = Depends(verify_firebase_token)):
    if not models["uci"]: raise HTTPException(503, "Model UCI not loaded")
    
    uid = token['uid']
    email = token.get('email')
    
    input_dict = data.dict(exclude={'phone_number'})
    
    try:
        probs = models["uci"].predict_proba(pd.DataFrame([input_dict]))
        risk_prob = float(probs[0][1])
    except Exception as e: raise HTTPException(400, f"Error: {e}")

    label = get_risk_message(risk_prob)
    
    # Save history and Send Email in Background (Speed Boost)
    background_tasks.add_task(save_history, uid, input_dict, risk_prob, label, "acute")
    background_tasks.add_task(send_email, email, risk_prob)
    
    return {"risk_probability": risk_prob, "risk_label": label, "alert_sent": True}

@app.post("/predict/lifestyle")
def predict_lifestyle(data: LifestyleInput, background_tasks: BackgroundTasks, token: dict = Depends(verify_firebase_token)):
    if not models["lifestyle"]: raise HTTPException(503, "Model Lifestyle not loaded")
    
    uid = token['uid']
    email = token.get('email')
    
    input_dict = data.dict(exclude={'phone_number'})
    
    # CRITICAL FIX: Cardio Train dataset uses age in DAYS. User inputs YEARS.
    # Convert Years -> Days
    input_dict['age'] = input_dict['age'] * 365
    
    height_m = input_dict['height'] / 100
    input_dict['bmi'] = input_dict['weight'] / (height_m * height_m)
    
    try:
        probs = models["lifestyle"].predict_proba(pd.DataFrame([input_dict]))
        risk_prob = float(probs[0][1])
    except Exception as e: raise HTTPException(400, f"Error: {e}")
    
    label = get_risk_message(risk_prob)
    
    # Background Tasks
    background_tasks.add_task(save_history, uid, input_dict, risk_prob, label, "lifestyle")
    background_tasks.add_task(send_email, email, risk_prob)
    
    return {"risk_probability": risk_prob, "risk_label": label}

@app.post("/predict/synthetic")
def predict_synthetic(data: SyntheticInput):
    # No Auth/History required for synthetic as per plan
    if not models["synthetic"]: raise HTTPException(503, "Model Synthetic not loaded")
    
    input_dict = data.dict()
    try:
        risk_score = float(models["synthetic"].predict(pd.DataFrame([input_dict]))[0])
        risk_score = max(0.0, min(1.0, risk_score)) # Clamp 0-1
    except Exception as e: raise HTTPException(400, f"Error: {e}")
    
    return {"risk_probability": risk_score, "risk_label": "Simulated Score"}

@app.get("/")
def read_root():
    return {"message": "Cardiac Prediction API is running"}
