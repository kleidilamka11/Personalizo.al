from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from app.dependencies.auth import is_admin

router = APIRouter()

@router.get("/admin/users")
def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(is_admin)
):
    return db.query(User).all()
