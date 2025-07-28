from pydantic import BaseModel, EmailStr
from typing import Optional


# Request model for user registration
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    is_admin: Optional[bool] = False


# Response model when returning user data (e.g. after register or login)
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_admin: bool
    is_verified: bool

    model_config = {
        "from_attributes": True  # ✅ Replaces orm_mode in Pydantic v2
    }


# 🧾 Schema for the login request (what the user sends)
class LoginRequest(BaseModel):
    email: EmailStr         # User will log in with email
    password: str           # Plaintext password they enter


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class VerifyRequest(BaseModel):
    token: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str
