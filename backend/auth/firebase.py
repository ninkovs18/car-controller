from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from google.oauth2 import id_token
from google.auth.transport import requests as grequests
import os

FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
bearer_scheme = HTTPBearer()

def verify_firebase_token(creds: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    try:
        token = creds.credentials
        info = id_token.verify_firebase_id_token(token, grequests.Request())
        if info.get("aud") != FIREBASE_PROJECT_ID and info.get("firebase", {}).get("project_id") != FIREBASE_PROJECT_ID:
            raise ValueError("Invalid project")
        return info
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or missing ID token")
