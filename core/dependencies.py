from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from core.jwt import decode_access_token
from sqlmodel import Session, select
from db import get_session
from models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> User:
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = session.exec(select(User).where(User.username == payload["sub"])).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def require_admin(user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return user

def require_active_user(user: User = Depends(get_current_user)):
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive account")
    return user