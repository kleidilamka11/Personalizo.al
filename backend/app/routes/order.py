from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.order import Order, OrderStatus
from app.models.song_package import SongPackage
from app.schemas.order import OrderCreate, OrderResponse
from app.db import get_db
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse)
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    package = db.query(SongPackage).filter(SongPackage.id == payload.song_package_id).first()
    if not package:
        raise HTTPException(404, detail="Song package not found")

    order = Order(
        user_id=current_user.id,
        song_package_id=payload.song_package_id,
        recipient_name=payload.recipient_name,
        mood=payload.mood,
        facts=payload.facts,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

@router.get("/me", response_model=List[OrderResponse])
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(Order).filter(Order.user_id == current_user.id).all()
