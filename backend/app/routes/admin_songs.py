from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status
from sqlalchemy.orm import Session
import os
from uuid import uuid4
import shutil

from app.db import get_db, BASE_DIR
from app.models.song import Song
from app.models.order import Order
from app.schemas.song import SongUploadResponse
from app.dependencies.auth import is_admin
from app.models.user import User
from app.core.config import settings
from app.core.email import send_email

router = APIRouter(prefix="/admin/songs", tags=["admin:songs"])

# Constants
MAX_FILE_SIZE_MB = 10
ALLOWED_MIME_TYPES = {"audio/mpeg", "audio/mp3"}


@router.post("/", response_model=SongUploadResponse)
async def upload_song(
    order_id: int = Form(...),
    title: str = Form(...),
    genre: str = Form(...),
    duration_seconds: int = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_admin: User = Depends(is_admin),
):
    # 1. Check if order exists
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # 2. Check if song already exists for this order
    existing_song = db.query(Song).filter(Song.order_id == order_id).first()
    if existing_song:
        raise HTTPException(status_code=400, detail="Song already exists for this order")

    # 3. Validate file type
    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # 4. Validate file size
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large (max 10MB)")
    file.file.seek(0)  # Reset pointer after read

    # 5. Save file to disk
    filename = f"song_{order_id}_{uuid4().hex}.mp3"
    file_location = BASE_DIR / "media" / "songs" / filename

    try:
        # Ensure the destination directory exists so file writes don't fail
        os.makedirs(file_location.parent, exist_ok=True)

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # 6. Create song in DB
        song = Song(
            order_id=order_id,
            title=title,
            genre=genre,
            duration_seconds=duration_seconds,
            file_path=str(file_location),
        )
        db.add(song)

        # 7. Mark order as delivered and store url
        order.status = "delivered"
        order.delivered_url = f"/media/songs/{filename}"

        db.commit()
        db.refresh(song)
        db.refresh(order)

        user = order.user
        if user:
            download_url = f"{settings.BASE_URL}/download{order.delivered_url}"
            send_email(
                to=user.email,
                subject="Your Personalizo.al song is ready",
                body=f"Your song is ready! Download it here: {download_url}",
            )

        # 8. Return response
        return SongUploadResponse(
            id=song.id,
            order_id=song.order_id,
            title=song.title,
            genre=song.genre,
            duration_seconds=song.duration_seconds,
            file_url=f"/media/songs/{filename}",
        )

    except Exception as e:
        if os.path.exists(file_location):
            os.remove(file_location)
        raise HTTPException(status_code=500, detail="Upload failed, please try again")
