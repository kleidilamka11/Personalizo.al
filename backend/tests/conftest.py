import os
import importlib
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import pytest

@pytest.fixture
def client(tmp_path):
    os.environ.setdefault("SECRET_KEY", "testsecret")
    os.environ.setdefault("ALGORITHM", "HS256")

    from app import db as db_module
    db_file = tmp_path / "test.db"
    engine = sqlalchemy.create_engine(f"sqlite:///{db_file}", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db_module.engine = engine
    db_module.SessionLocal = TestingSessionLocal

    from app.models.user import Base
    Base.metadata.create_all(bind=engine)

    import app.main as main_module
    importlib.reload(main_module)

    from fastapi.testclient import TestClient
    return TestClient(main_module.app)
