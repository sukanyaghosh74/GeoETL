from fastapi import Header, HTTPException, status
from backend.app.core.config import settings

def verify_api_key(x_geoetl_apikey: str = Header(...)):
    if x_geoetl_apikey != settings.API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
