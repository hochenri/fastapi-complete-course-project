from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from db import get_session
from models.user import User
from core.dependencies import require_admin

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users", dependencies=[Depends(require_admin)])
def list_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()