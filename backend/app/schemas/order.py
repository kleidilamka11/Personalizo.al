from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from datetime import datetime

# ---------- Enums ----------
class OrderStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    delivered = "delivered"
    cancelled = "cancelled"

# ---------- Base Order ----------
class OrderBase(BaseModel):
    song_package_id: int
    recipient_name: str
    mood: str
    facts: Optional[str]

# ---------- Order Create ----------
class OrderCreate(OrderBase):
    pass

# ---------- Order Response ----------
class OrderResponse(OrderBase):
    id: int
    status: OrderStatus
    delivered_url: Optional[str]

    model_config = {
        "from_attributes": True
    }

# ---------- Admin Preview Schemas ----------
class UserPreview(BaseModel):
    id: int
    email: str

class PackagePreview(BaseModel):
    id: int
    name: str

# ---------- Admin Order Out ----------
class AdminOrderOut(BaseModel):
    id: int
    recipient_name: str
    mood: Optional[str]
    facts: Optional[str]
    status: OrderStatus
    delivered_url: Optional[str]
    created_at: datetime

    user: UserPreview
    package: PackagePreview

    model_config = {
        "from_attributes": True
    }
