from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session, select
from models.user import User
from db import get_session
from core.security import hash_password, verify_password
from fastapi.security import OAuth2PasswordRequestForm
from core.jwt import create_access_token

# SlowAPI imports
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter(prefix="/auth", tags=["Auth"])

# Create limiter instance for this router
limiter = Limiter(key_func=get_remote_address)

@router.post("/signup", status_code=201)
@limiter.limit("3/minute")   # limit signup attempts per IP
def signup(request: Request, user: User, session: Session = Depends(get_session)):
    existing_user = session.exec(select(User).where(User.username == user.username)).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    user.hashed_password = hash_password(user.hashed_password)
    # Add user role
    user.role = user.role or "user"  # default to "user"
    
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": "User created", "user_id": user.id}

@router.post("/login")
@limiter.limit("5/minute")   # limit login attempts per IP
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.username == form_data.username)).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}