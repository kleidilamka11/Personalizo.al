from fastapi import Depends, HTTPException, status
from app.models.user import User
from app.routes.auth import get_current_user  # Adjust if located elsewhere

def is_admin(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admins only"
        )
    return current_user
