from fastapi import APIRouter, Depends, HTTPException, status, Header
from firebase_admin import auth
from .utils import ACCESS_TOKEN_EXPIRE_MINUTES # Not really needed anymore but ok
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/auth", tags=["Authentication"])

class UserResponse(BaseModel):
    uid: str
    email: str
    
# Dependency to verify Firebase ID Token
async def verify_firebase_token(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = authorization.split(" ")[1]
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

# We can keep a 'me' endpoint for testing token validity
@router.get("/me")
def read_users_me(decoded_token: dict = Depends(verify_firebase_token)):
    return {
        "uid": decoded_token.get("uid"),
        "email": decoded_token.get("email"),
        "message": "Firebase Token Valid"
    }

# Signup/Login is now handled on Frontend via Firebase SDK. 
# We might want an endpoint to sync User data to Firestore if not done purely by FE.
# For now, we trust the Token.

