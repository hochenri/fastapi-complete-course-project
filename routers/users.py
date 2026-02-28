from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from db import get_session
from core.dependencies import require_admin
from models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/admin/users", dependencies=[Depends(require_admin)])
def list_all_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()