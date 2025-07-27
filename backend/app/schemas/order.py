from pydantic import BaseModel
from typing import Optional
from enum import Enum

class OrderStatus(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    delivered = "delivered"
    cancelled = "cancelled"

class OrderBase(BaseModel):
    song_package_id: int
    recipient_name: str
    mood: str
    facts: Optional[str]

class OrderCreate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: int
    status: OrderStatus
    delivered_url: Optional[str]

    model_config = {
        "from_attributes": True
    }