from pydantic import BaseModel
from typing import Optional

class SongPackageBase(BaseModel):
    tier: str
    name: str
    description: Optional[str]
    price_eur: int
    duration_seconds: int
    commercial_use: bool

class SongPackageResponse(SongPackageBase):
    id: int

    class Config:
        orm_mode = True
