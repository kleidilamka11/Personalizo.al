from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.schemas.song import SongCreate, SongResponse
from app.models.song import Song
from app.models.order import Order
from app.models.user import User
from app.db import get_db
from app.core.security import get_current_user

router = APIRouter(prefix="/songs", tags=["Songs"])


@router.post("/", response_model=SongResponse)
def create_song(song: SongCreate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == song.order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if db.query(Song).filter(Song.order_id == song.order_id).first():
        raise HTTPException(status_code=400, detail="Song already exists for this order")

    new_song = Song(**song.model_dump())
    db.add(new_song)
    db.commit()
    db.refresh(new_song)
    return new_song


@router.get("/", response_model=List[SongResponse])
def list_songs(db: Session = Depends(get_db)):
    return db.query(Song).all()


@router.get("/me", response_model=List[SongResponse])
def get_my_songs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    songs = (
        db.query(Song)
        .join(Order)
        .filter(Order.user_id == current_user.id)
        .all()
    )
    return songs


@router.get("/{order_id}", response_model=SongResponse)
def get_song_by_order(order_id: int, db: Session = Depends(get_db)):
    song = db.query(Song).filter(Song.order_id == order_id).first()
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song