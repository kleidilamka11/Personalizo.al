from pydantic import BaseModel
from typing import Optional

class SongPackageBase(BaseModel):
    tier: str
    name: str
    description: Optional[str]
    price_eur: int
    duration_seconds: int
    commercial_use: bool
    lemon_squeezy_variant_id: Optional[int] | None = None

class SongPackageResponse(SongPackageBase):
    id: int
    model_config = {
        "from_attributes": True
    }


class SongPackageUpdate(BaseModel):
    tier: str | None = None
    name: str | None = None
    description: str | None = None
    price_eur: int | None = None
    duration_seconds: int | None = None
    commercial_use: bool | None = None
    lemon_squeezy_variant_id: int | None = None
