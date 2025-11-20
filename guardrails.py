# OAuth2 and IP whitelist guardrails for production security

from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ALLOWED_IPS: List[str] = ["127.0.0.1", "::1", "192.168.1.100"]

def validate_ip(client_ip: str):
    """Validate client IP against whitelist."""
    if client_ip not in ALLOWED_IPS:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"IP {client_ip} not whitelisted"
        )

def get_current_user(token: str = Depends(oauth2_scheme)):
    """Validate OAuth2 token (mock implementation)."""
    if token != "fake-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return {"username": "quant_user", "role": "analyst"}
