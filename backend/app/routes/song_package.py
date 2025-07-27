from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.song_package import SongPackage
from app.schemas.song_package import SongPackageResponse, SongPackageBase

router = APIRouter(prefix="/packages", tags=["Song Packages"])

@router.get("/", response_model=List[SongPackageResponse])
def get_song_packages(db: Session = Depends(get_db)):
    return db.query(SongPackage).all()

@router.post("/", response_model=SongPackageResponse)
def create_song_package(
    payload: SongPackageBase,
    db: Session = Depends(get_db)
):
    existing = db.query(SongPackage).filter(SongPackage.tier == payload.tier).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tier already exists.")

    new_package = SongPackage(**payload.model_dump())
    db.add(new_package)
    db.commit()
    db.refresh(new_package)
    return new_package
