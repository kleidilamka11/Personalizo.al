from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SongBase(BaseModel):
    order_id: int
    title: str
    genre: Optional[str] = "unknown"
    duration_seconds: Optional[int] = None
    file_path: str


class SongCreate(SongBase):
    pass


class SongResponse(SongBase):
    id: int
    created_at: datetime
    model_config = {
        "from_attributes": True
    }


class SongUploadResponse(BaseModel):
    id: int
    order_id: int
    title: str
    genre: str
    duration_seconds: Optional[int]
    file_url: str

    model_config = {
        "from_attributes": True
    }


class SongUpdate(BaseModel):
    order_id: int | None = None
    title: str | None = None
    genre: str | None = None
    duration_seconds: int | None = None
    file_path: str | None = None
