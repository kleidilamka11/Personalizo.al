# backend/scripts/seed_data.py

from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models.song_package import SongPackage
from app.models.user import User
from app.models.order import Order
from app.models.song import Song
from app.core.security import hash_password
from datetime import datetime, timezone

db: Session = SessionLocal()

# 1. Create an admin user
admin = db.query(User).filter_by(email="admin@personalizo.al").first()
if not admin:
    admin = User(
        email="admin@personalizo.al",
        username="admin",
        hashed_password=hash_password("admin123"),
        is_admin=True
    )
    db.add(admin)
    print("✅ Admin created")

# 2. Create a song package
package = db.query(SongPackage).first()
if not package:
    package = SongPackage(
    tier="full_personal",
    name="Full Personal",
    description="A complete personalized song for personal use",
    price_eur=1999,
    duration_seconds=180,
    commercial_use=False
)
    db.add(package)
    print("✅ SongPackage created")

db.commit()

# 3. Create a test user
user = db.query(User).filter_by(email="test@user.com").first()
if not user:
    user = User(
        email="test@user.com",
        username="testuser",
        hashed_password=hash_password("test1234"),
        is_admin=False
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print("✅ Test user created")

# 4. Create a sample order
order = db.query(Order).first()
if not order:
    order = Order(
        user_id=user.id,
        song_package_id=package.id,
        recipient_name="Arta",
        mood="Joyful",
        facts="Loves sunsets and poetry",
        status="pending",
        created_at=datetime.now(timezone.utc)
    )
    db.add(order)
    db.commit()
    print("✅ Order created")

db.close()
