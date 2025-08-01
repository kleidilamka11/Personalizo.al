import os
import importlib
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import pytest
import sys
from pathlib import Path
import warnings
os.environ.setdefault("SECRET_KEY", "testsecret")
os.environ.setdefault("ALGORITHM", "HS256")
os.environ.setdefault("LEMONSQUEEZY_API_KEY", "test")
os.environ.setdefault("LEMONSQUEEZY_STORE_ID", "1")

import app.routes.auth as auth_routes

class DummyRedis:
    def __init__(self):
        self.store = {}
    def incr(self, key):
        self.store[key] = self.store.get(key, 0) + 1
        return self.store[key]
    def expire(self, key, seconds):
        pass
    def scan_iter(self, match=None):
        return list(self.store.keys())
    def delete(self, key):
        self.store.pop(key, None)

auth_routes.limiter.redis = DummyRedis()

# Ensure the backend directory is on sys.path so that "import app" works even
# when tests are invoked from the repository root.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# Silence deprecation warnings from third-party libraries
warnings.filterwarnings("ignore", category=DeprecationWarning, module="passlib")


@pytest.fixture
def db(tmp_path):
    os.environ.setdefault("SECRET_KEY", "testsecret")
    os.environ.setdefault("ALGORITHM", "HS256")

    from app import db as db_module
    db_file = tmp_path / "test.db"
    engine = sqlalchemy.create_engine(
        f"sqlite:///{db_file}", connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db_module.engine = engine
    db_module.SessionLocal = TestingSessionLocal

    from app.db import Base
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def client(db):
    import app.main as main_module
    importlib.reload(main_module)

    from fastapi.testclient import TestClient
    return TestClient(main_module.app)


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    yield
    auth_routes.limiter.reset()
