# Importing base tools from SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.db import Base

# This defines our User table in the database
class User(Base):
    __tablename__ = "users"  # The table will be called 'users'

    # Primary key (auto-incremented integer)
    id = Column(Integer, primary_key=True, index=True)

    # Email address of the user - must be unique and not null
    email = Column(String, unique=True, index=True, nullable=False)

    # Public username - must be unique and not null
    username = Column(String, unique=True, index=True, nullable=False)

    # Password will be stored hashed (NEVER plain!) - not null
    hashed_password = Column(String, nullable=False)

    # Timestamp of when the user was created - default is current time
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Check if user is admin - default is false
    is_admin = Column(Boolean, default=False)
