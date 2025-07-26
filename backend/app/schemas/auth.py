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

    model_config = {
        "from_attributes": True  # ✅ Replaces orm_mode in Pydantic v2
    }

from pydantic import BaseModel, EmailStr

# 🧾 Schema for the login request (what the user sends)
class LoginRequest(BaseModel):
    email: EmailStr         # User will log in with email
    password: str           # Plaintext password they enter


# 🔐 Schema for the login response (what we send back)
class TokenResponse(BaseModel):
    access_token: str       # JWT access token
    token_type: str         # Usually "bearer"
