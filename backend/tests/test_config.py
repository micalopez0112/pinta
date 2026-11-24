import pytest

from app.config import Settings


@pytest.mark.parametrize(
    ("given", "expected"),
    [
        # Neon / Render / Heroku entregan estas formas: hay que agregarles el driver.
        ("postgresql://u:p@host/db?sslmode=require", "postgresql+psycopg://u:p@host/db?sslmode=require"),
        ("postgres://u:p@host/db", "postgresql+psycopg://u:p@host/db"),
        # Lo que ya está bien (o no es Postgres) no se toca.
        ("postgresql+psycopg://u:p@host/db", "postgresql+psycopg://u:p@host/db"),
        ("sqlite://", "sqlite://"),
    ],
)
def test_database_url_gets_the_psycopg_driver(given, expected):
    assert Settings(database_url=given).database_url == expected


def test_cors_origins_are_split_and_trimmed():
    settings = Settings(cors_origins="https://pinta.pages.dev, http://localhost:5173 ,")
    assert settings.cors_origin_list == ["https://pinta.pages.dev", "http://localhost:5173"]
