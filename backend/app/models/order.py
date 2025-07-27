from sqlalchemy import Column, Integer, String, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from app.db import Base
import enum


class OrderStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    delivered = "delivered"
    cancelled = "cancelled"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    song_package_id = Column(Integer, ForeignKey("song_packages.id"), nullable=False)
    song = relationship("Song", back_populates="order", uselist=False)


    recipient_name = Column(String, nullable=False)
    mood = Column(String, nullable=False)
    facts = Column(Text, nullable=True)

    status = Column(Enum(OrderStatus), default=OrderStatus.pending)
    delivered_url = Column(String, nullable=True)

    # relationships
    user = relationship("User", back_populates="orders")
    song_package = relationship("SongPackage")

    
