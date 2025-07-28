from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from app.schemas.auth import (
    UserCreate,
    UserResponse,
    LoginRequest,
    TokenResponse,
    VerifyRequest,
    PasswordResetRequest,
    PasswordResetConfirm,
)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    get_current_user,
)
from app.core.limiter import RateLimiter
import uuid
from datetime import datetime, timedelta, timezone
import os
from jose import jwt, JWTError
from app.core.config import settings
from pydantic import BaseModel


router = APIRouter(prefix="/auth", tags=["auth"])

# Simple global rate limiter applied to auth-related endpoints
limiter = RateLimiter(max_requests=5, window_seconds=60)




# ✅ Register route
@router.post("/register", response_model=UserResponse)
def register(
    user_data: UserCreate,
    request: Request,
    db: Session = Depends(get_db),
    _: None = Depends(limiter),
):
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email or username already taken")

    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
        is_admin=user_data.is_admin,
    )

    # generate a verification token for email confirmation
    new_user.verification_token = str(uuid.uuid4())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# ✅ JSON login route (from frontend)
@router.post("/login", response_model=TokenResponse)
def login_user(
    login_data: LoginRequest,
    request: Request,
    db: Session = Depends(get_db),
    _: None = Depends(limiter),
):
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# ✅ OAuth2 token route for Swagger UI login
@router.post("/token", response_model=TokenResponse)
def login_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    request: Request = None,
    db: Session = Depends(get_db),
    _: None = Depends(limiter),
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


# ✅ Authenticated user info route
@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user



class RefreshTokenRequest(BaseModel):
    refresh_token: str

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    data: RefreshTokenRequest,
    request: Request,
    db: Session = Depends(get_db),
    _: None = Depends(limiter),
):
    try:
        payload = jwt.decode(data.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    new_access_token = create_access_token(data={"sub": user.email})
    new_refresh_token = create_refresh_token(data={"sub": user.email})

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


# -------------------- Verification Endpoints --------------------

@router.post("/request-verify")
def request_verification(
    data: PasswordResetRequest,
    request: Request,
    db: Session = Depends(get_db),
    _: None = Depends(limiter),
):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.verification_token = str(uuid.uuid4())
    db.commit()
    return {"token": user.verification_token}


@router.post("/verify")
def verify_account(
    payload: VerifyRequest,
    request: Request,
    db: Session = Depends(get_db),
    _: None = Depends(limiter),
):
    user = db.query(User).filter(User.verification_token == payload.token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")
    user.is_verified = True
    user.verification_token = None
    db.commit()
    return {"message": "verified"}


# -------------------- Password Reset Endpoints --------------------

@router.post("/password-reset-request")
def password_reset_request(
    data: PasswordResetRequest,
    request: Request,
    db: Session = Depends(get_db),
    _: None = Depends(limiter),
):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.reset_token = str(uuid.uuid4())
    user.reset_token_expires = datetime.now(timezone.utc) + timedelta(hours=1)
    db.commit()
    return {"token": user.reset_token}


@router.post("/password-reset")
def password_reset(
    data: PasswordResetConfirm,
    request: Request,
    db: Session = Depends(get_db),
    _: None = Depends(limiter),
):
    user = db.query(User).filter(User.reset_token == data.token).first()
    if not user or not user.reset_token_expires or user.reset_token_expires < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Invalid token")
    user.hashed_password = hash_password(data.new_password)
    user.reset_token = None
    user.reset_token_expires = None
    db.commit()
    return {"message": "password updated"}


