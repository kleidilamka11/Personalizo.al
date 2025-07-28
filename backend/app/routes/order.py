from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.order import Order, OrderStatus
from app.models.song_package import SongPackage
from app.schemas.order import OrderCreate, OrderResponse, OrderUpdate, OrderCancel
from app.db import get_db
from app.models.user import User
from app.core.security import get_current_user


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


@router.patch("/{order_id}", response_model=OrderResponse)
def update_order(
    order_id: int,
    payload: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this order")
    if order.status != OrderStatus.pending:
        raise HTTPException(status_code=400, detail="Only pending orders can be updated")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(order, field, value)
    db.commit()
    db.refresh(order)
    return order


@router.post("/{order_id}/cancel", response_model=OrderResponse)
def cancel_order(
    order_id: int,
    payload: OrderCancel | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to cancel this order")
    if order.status == OrderStatus.delivered:
        raise HTTPException(status_code=400, detail="Delivered orders cannot be cancelled")
    if order.status == OrderStatus.cancelled:
        raise HTTPException(status_code=400, detail="Order already cancelled")

    order.status = OrderStatus.cancelled
    db.commit()
    db.refresh(order)
    return order
