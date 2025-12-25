from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from .database import get_db
from .auth.routes import verify_firebase_token
import datetime

router = APIRouter(prefix="/profile", tags=["Profile"])

class ProfileBase(BaseModel):
    age: int
    gender: str
    height: float
    weight: float
    medical_conditions: Optional[str] = None
    stress_level: int
    glucose: int = 1
    smoke: int = 0
    alco: int = 0
    active: int = 1

class ProfileResponse(ProfileBase):
    bmi: float
    
class PredictionResponse(BaseModel):
    id: str
    timestamp: str 
    risk_label: str
    risk_probability: float
    model_type: Optional[str] = "acute"

@router.get("/", response_model=Optional[ProfileResponse])
def get_my_profile(token: dict = Depends(verify_firebase_token)):
    uid = token['uid']
    db = get_db()
    
    # Path: users/{uid}/data/profile
    doc_ref = db.collection('users').document(uid).collection('data').document('profile')
    doc = doc_ref.get()
    
    if doc.exists:
        return doc.to_dict()
    return None

@router.post("/", response_model=ProfileResponse)
def create_or_update_profile(profile_data: ProfileBase, token: dict = Depends(verify_firebase_token)):
    uid = token['uid']
    db = get_db()
    
    # Calculate BMI
    height_m = profile_data.height / 100
    bmi = round(profile_data.weight / (height_m * height_m), 2)
    
    data = profile_data.dict()
    data['bmi'] = bmi
    
    # Save to Firestore
    doc_ref = db.collection('users').document(uid).collection('data').document('profile')
    doc_ref.set(data, merge=True)
    
    # Also ensure the user document exists with basic info from token if not already
    user_ref = db.collection('users').document(uid)
    if not user_ref.get().exists:
        user_ref.set({
            'email': token.get('email'),
            'uid': uid
        }, merge=True)
        
    return data

@router.get("/history", response_model=List[PredictionResponse])
def get_history(token: dict = Depends(verify_firebase_token)):
    uid = token['uid']
    db = get_db()
    
    preds_ref = db.collection('users').document(uid).collection('predictions').order_by('timestamp', direction='DESCENDING')
    docs = preds_ref.stream()
    
    history = []
    for doc in docs:
        p = doc.to_dict()
        p['id'] = doc.id
        # Ensure timestamp is string for response
        if 'timestamp' in p and not isinstance(p['timestamp'], str):
             p['timestamp'] = str(p['timestamp'])
        history.append(p)
        
    return history
