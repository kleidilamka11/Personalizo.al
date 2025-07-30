from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session
from typing import List

from app.db import get_db
from app.models.song_package import SongPackage
from app.schemas.song_package import (
    SongPackageResponse,
    SongPackageBase,
    SongPackageUpdate,
)

router = APIRouter(prefix="/packages", tags=["Song Packages"])

@router.get("/", response_model=List[SongPackageResponse])
def get_song_packages(db: Session = Depends(get_db)):
    return db.query(SongPackage).all()


@router.get("/{package_id}", response_model=SongPackageResponse)
def get_song_package(package_id: int, db: Session = Depends(get_db)):
    package = db.query(SongPackage).filter(SongPackage.id == package_id).first()
    if not package:
        raise HTTPException(status_code=404, detail="Song package not found")
    return package

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


@router.put("/{package_id}", response_model=SongPackageResponse)
def update_song_package(
    package_id: int,
    payload: SongPackageUpdate,
    db: Session = Depends(get_db),
):
    package = db.query(SongPackage).filter(SongPackage.id == package_id).first()
    if not package:
        raise HTTPException(status_code=404, detail="Song package not found")

    if payload.tier and payload.tier != package.tier:
        existing = db.query(SongPackage).filter(SongPackage.tier == payload.tier).first()
        if existing:
            raise HTTPException(status_code=400, detail="Tier already exists.")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(package, field, value)
    db.commit()
    db.refresh(package)
    return package


@router.delete("/{package_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_song_package(package_id: int, db: Session = Depends(get_db)):
    package = db.query(SongPackage).filter(SongPackage.id == package_id).first()
    if not package:
        raise HTTPException(status_code=404, detail="Song package not found")
    db.delete(package)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
