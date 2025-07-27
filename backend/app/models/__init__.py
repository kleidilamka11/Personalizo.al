
"""Convenience exports for model classes.

This module exposes the individual SQLAlchemy models so that other
parts of the application can simply import ``app.models`` and access
``User``, ``Order`` and the rest directly.  The tests for the admin
routes rely on this behaviour when they call ``db.query(models.Order)``.
"""

from .user import User
from .order import Order, OrderStatus
from .song import Song
from .song_package import SongPackage

__all__ = [
    "User",
    "Order",
    "OrderStatus",
    "Song",
    "SongPackage",
]
