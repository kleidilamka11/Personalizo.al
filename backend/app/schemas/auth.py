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
