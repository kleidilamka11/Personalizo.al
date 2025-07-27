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

    class Config:
        from_attributes = True
