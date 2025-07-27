from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.db import Base


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    title = Column(String, nullable=False)
    genre = Column(String, default="unknown")
    duration_seconds = Column(Integer, nullable=True)
    file_path = Column(String, nullable=False)

    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    order = relationship("Order", back_populates="song")

