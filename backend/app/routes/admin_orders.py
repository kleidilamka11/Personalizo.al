from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app import models, schemas
from app.models.user import User
from app.dependencies.auth import is_admin
from app.db import get_db

router = APIRouter(prefix="/admin/orders", tags=["admin:orders"])


@router.get("/", response_model=List[schemas.order.AdminOrderOut])
def get_all_orders(
    status: Optional[str] = Query(None),
    user_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_admin: User = Depends(is_admin),
):
    query = db.query(models.Order).join(models.User).join(models.SongPackage)

    if status:
        query = query.filter(models.Order.status == status)
    if user_id:
        query = query.filter(models.Order.user_id == user_id)

    orders = query.all()

    return [
        schemas.order.AdminOrderOut(
            id=o.id,
            recipient_name=o.recipient_name,
            mood=o.mood,
            facts=o.facts,
            status=o.status,
            delivered_url=o.delivered_url,
            created_at=o.created_at,
            user={"id": o.user.id, "email": o.user.email},
            package={"id": o.package.id, "title": o.package.title},
        )
        for o in orders
    ]
