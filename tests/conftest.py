import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from main import app
from core.db import Base, get_db
from models import Menu, Submenu, Dish
from config import DATABASE_URL


engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
client = TestClient(app)


@pytest.fixture(scope="module")
def client():
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def db():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(autouse=True)
def clean_db(db: Session):
    yield
    db.rollback()
    db.query(Submenu).delete()
    db.query(Menu).delete()
    db.query(Dish).delete()
    db.commit()


@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    """Очистка базы данных после тестов"""
    def drop_tables():
        Base.metadata.drop_all(bind=engine)
    request.addfinalizer(drop_tables)
