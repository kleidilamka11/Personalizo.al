from sqlalchemy import Column, Integer, String, Boolean
from app.db import Base

class SongPackage(Base):
    __tablename__ = "song_packages"

    id = Column(Integer, primary_key=True, index=True)
    tier = Column(String, unique=True, index=True)  # short_personal, full_personal, full_commercial
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price_eur = Column(Integer, nullable=False)
    duration_seconds = Column(Integer, nullable=False)
    commercial_use = Column(Boolean, default=False)
    lemon_squeezy_variant_id = Column(String, nullable=True)
