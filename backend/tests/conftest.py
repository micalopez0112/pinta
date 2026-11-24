import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app import weather
from app.database import Base, get_db
from app.main import app
from app.seed import seed

# Respuesta de ejemplo de Open-Meteo (recortada a lo que usamos).
FAKE_FORECAST = {
    "current": {
        "time": "2026-11-23T15:00",
        "temperature_2m": 27.4,
        "apparent_temperature": 28.0,
        "is_day": 1,
        "weather_code": 1,
        "wind_speed_10m": 12.5,
    },
    "daily": {
        "temperature_2m_max": [28.1],
        "temperature_2m_min": [17.0],
        "precipitation_probability_max": [5],
        "uv_index_max": [9.1],
        "sunset": ["2026-11-23T19:31"],
    },
}


@pytest.fixture()
def db_session():
    # SQLite en memoria: los tests no necesitan Postgres.
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    with sessionmaker(bind=engine, expire_on_commit=False)() as session:
        seed(session)
        yield session


@pytest.fixture()
def client(db_session):
    app.dependency_overrides[get_db] = lambda: db_session
    weather._cache.clear()
    # Sin `with`, TestClient no ejecuta el lifespan (que intentaría conectarse a Postgres).
    yield TestClient(app)
    app.dependency_overrides.clear()
    weather._cache.clear()
