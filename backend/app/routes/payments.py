from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import httpx

from app.db import get_db
from app.models.order import Order
from app.models.user import User
from app.core.security import get_current_user
from app.core.config import settings
from app.schemas.payment import CheckoutResponse

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/checkout/{order_id}", response_model=CheckoutResponse)
def create_checkout(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    variant_id = order.song_package.lemon_squeezy_variant_id
    if not variant_id:
        raise HTTPException(status_code=400, detail="Package not configured for payments")

    if not settings.LEMONSQUEEZY_API_KEY or not settings.LEMONSQUEEZY_STORE_ID:
        raise HTTPException(status_code=500, detail="Payment provider not configured")

    payload = {
        "checkout": {
            "store_id": settings.LEMONSQUEEZY_STORE_ID,
            "variant_id": variant_id,
            "custom": {"order_id": order.id, "user_id": current_user.id},
            "redirect_url": f"{settings.BASE_URL}/orders",
            "cancel_url": f"{settings.BASE_URL}/cart",
        }
    }

    headers = {
        "Authorization": f"Bearer {settings.LEMONSQUEEZY_API_KEY}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }

    response = httpx.post("https://api.lemonsqueezy.com/v1/checkouts", json=payload, headers=headers)
    if response.status_code not in (200, 201):
        raise HTTPException(status_code=502, detail="Failed to create checkout")
    data = response.json()
    url = data.get("data", {}).get("attributes", {}).get("url")
    if not url:
        raise HTTPException(status_code=502, detail="Invalid checkout response")
    return CheckoutResponse(url=url)
