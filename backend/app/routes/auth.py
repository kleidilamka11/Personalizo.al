from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.user import User
from app.schemas.auth import UserCreate, UserResponse, LoginRequest, TokenResponse
from app.core.security import hash_password, verify_password, create_access_token, get_current_user  
from app.schemas.auth import LoginRequest, TokenResponse
from datetime import timedelta
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from app.core.security import get_current_user
from fastapi.security import OAuth2PasswordRequestForm



load_dotenv()


router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

# Dependency: get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if user with same email or username already exists
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already taken."
        )

    # Create new user object with hashed password
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hash_password(user_data.password),
        is_admin=user_data.is_admin
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

#LOGIN ROUTE
@router.post("/login", response_model=TokenResponse)
def login_user(login_data: LoginRequest, db: Session = Depends(get_db)):
    # 🔍 Step 1: Look up the user
    user = db.query(User).filter(User.email == login_data.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # 🔐 Step 2: Check password
    if not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # 🧾 Step 3: Create token
    token_expiry = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)))
    token = create_access_token(data={"sub": user.email}, expires_delta=token_expiry)

    # ✅ Step 4: Return token
    return {"access_token": token, "token_type": "bearer"}


# Is User Logged in Route


@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.post("/token", response_model=TokenResponse)
def login_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
