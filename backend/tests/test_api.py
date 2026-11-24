import httpx
import pytest
from sqlalchemy import func, select

from app import models, weather
from app.config import settings
from app.seed import seed
from app.seed_data import DESTINATIONS

from .conftest import FAKE_FORECAST

SLUG = "punta-del-este"
SEEDED_ACTIVITIES = len(DESTINATIONS[0]["activities"])


def test_health(client):
    assert client.get("/api/health").json() == {"status": "ok"}


def test_ping_works_even_if_the_database_is_down(client):
    from app.database import get_db
    from app.main import app

    def broken_db():
        raise RuntimeError("/api/ping no debería tocar la base")

    app.dependency_overrides[get_db] = broken_db  # el fixture `client` lo restablece al terminar
    assert client.get("/api/ping").json() == {"status": "ok"}


def test_categories(client):
    data = client.get("/api/categories").json()
    assert {"slug": "playa", "label": "Playas"} in data


@pytest.mark.parametrize(
    ("lang", "label"),
    [("en", "Beaches"), ("pt", "Praias"), ("de", "Strände"), ("es", "Playas"), ("pt-BR", "Praias"), ("xx", "Playas")],
)
def test_categories_by_language(client, lang, label):
    data = client.get("/api/categories", params={"lang": lang}).json()
    assert {"slug": "playa", "label": label} in data
    # mismo orden en todos los idiomas
    assert [c["slug"] for c in data] == ["playa", "paseo", "cultura", "naturaleza", "restaurante", "supermercado"]


def test_destination(client):
    data = client.get(f"/api/destinations/{SLUG}").json()
    assert data["name"] == "Punta del Este"
    assert client.get("/api/destinations/narnia").status_code == 404


def test_list_activities(client):
    data = client.get(f"/api/destinations/{SLUG}/activities").json()
    assert len(data) == SEEDED_ACTIVITIES
    assert data[0]["slug"] == "la-mano-playa-brava"


def _by_slug(client, lang=None):
    params = {"lang": lang} if lang else {}
    data = client.get(f"/api/destinations/{SLUG}/activities", params=params).json()
    return {a["slug"]: a for a in data}


@pytest.mark.parametrize(
    ("lang", "title", "zone"),
    [
        ("en", "Port and sea lions", "Port"),
        ("pt", "Porto e lobos-marinhos", "Porto"),
        ("de", "Hafen und Seelöwen", "Hafen"),
        ("es", "Puerto y lobos marinos", "Puerto"),
    ],
)
def test_activities_in_each_language(client, lang, title, zone):
    activity = _by_slug(client, lang)["puerto-punta-del-este"]
    assert activity["title"] == title
    assert activity["zone"] == zone


def test_unknown_language_falls_back_to_spanish(client):
    assert _by_slug(client, "xx") == _by_slug(client)  # sin ?lang= es español


def test_untranslated_fields_fall_back_to_spanish(client):
    # "Isla Gorriti" es un nombre propio: no tiene título traducido, pero sí descripción.
    spanish = _by_slug(client)["isla-gorriti"]
    english = _by_slug(client, "en")["isla-gorriti"]
    assert english["title"] == spanish["title"] == "Isla Gorriti"
    assert english["description"] != spanish["description"]


def test_translation_does_not_change_non_text_fields(client):
    spanish, german = _by_slug(client), _by_slug(client, "de")
    for slug, activity in spanish.items():
        for field in ("id", "category", "latitude", "longitude", "price_level", "indoor"):
            assert german[slug][field] == activity[field]


def test_every_activity_is_translated_into_every_language(client):
    for lang in ("en", "pt", "de"):
        for slug, activity in _by_slug(client, lang).items():
            spanish = _by_slug(client)[slug]
            assert activity["description"] != spanish["description"], f"{slug} sin traducir al {lang}"


def test_filter_by_category(client):
    data = client.get(f"/api/destinations/{SLUG}/activities", params={"category": "playa"}).json()
    assert data
    assert {a["category"] for a in data} == {"playa"}


def test_filter_indoor(client):
    data = client.get(f"/api/destinations/{SLUG}/activities", params={"indoor": True}).json()
    assert [a["slug"] for a in data] == [
        "museo-ralli", "museo-del-mar", "zazu-puerto", "lo-de-tere", "virazon", "la-posta-del-cangrejo",
    ]  # fmt: skip


def test_restaurants(client):
    data = client.get(f"/api/destinations/{SLUG}/activities", params={"category": "restaurante"}).json()
    assert "zazu-puerto" in [a["slug"] for a in data]
    assert len(data) >= 3


def test_supermarkets_are_not_rainy_day_plans(client):
    supermarkets = client.get(f"/api/destinations/{SLUG}/activities", params={"category": "supermercado"}).json()
    assert len(supermarkets) >= 3
    assert not any(a["indoor"] for a in supermarkets)


def test_every_place_is_inside_the_map_area(client):
    # Detecta una coordenada mal cargada (por ejemplo, con el signo cambiado): todo tiene que
    # caer entre Punta Ballena, La Barra y la Isla de Lobos.
    for slug, a in _by_slug(client).items():
        assert -35.05 < a["latitude"] < -34.85, slug
        assert -55.06 < a["longitude"] < -54.80, slug


def test_activities_of_unknown_destination(client):
    assert client.get("/api/destinations/narnia/activities").status_code == 404


def test_seed_is_idempotent(db_session):
    seed(db_session)
    seed(db_session)
    assert db_session.scalar(select(func.count()).select_from(models.Activity)) == SEEDED_ACTIVITIES


def test_weather(client, monkeypatch):
    calls = []

    def fake_fetch(*args):
        calls.append(args)
        return FAKE_FORECAST

    monkeypatch.setattr(weather, "fetch_forecast", fake_fetch)

    data = client.get(f"/api/destinations/{SLUG}/weather").json()
    assert data["temperature"] == 27.4
    assert data["condition"] == "mainly_clear"  # una clave: el frontend la traduce
    assert data["icon"] == "clear"
    assert data["sunset"] == "19:31"
    assert data["suggestion"] == "beach"

    client.get(f"/api/destinations/{SLUG}/weather")
    assert len(calls) == 1  # la segunda salió de la caché


def test_weather_upstream_down(client, monkeypatch):
    def boom(*args):
        raise httpx.ConnectError("sin red")

    monkeypatch.setattr(weather, "fetch_forecast", boom)
    assert client.get(f"/api/destinations/{SLUG}/weather").status_code == 502


def test_weather_serves_stale_data_when_upstream_fails(client, monkeypatch):
    monkeypatch.setattr(settings, "weather_cache_seconds", 0)  # la caché siempre "vence"
    monkeypatch.setattr(weather, "fetch_forecast", lambda *a: FAKE_FORECAST)
    assert client.get(f"/api/destinations/{SLUG}/weather").status_code == 200

    def boom(*args):
        raise httpx.ConnectError("sin red")

    monkeypatch.setattr(weather, "fetch_forecast", boom)
    response = client.get(f"/api/destinations/{SLUG}/weather")
    assert response.status_code == 200
    assert response.json()["temperature"] == 27.4


@pytest.mark.parametrize(
    ("icon", "temp", "rain", "wind", "is_day", "expected"),
    [
        ("rain", 26, 90, 10, True, "indoor"),
        ("clear", 26, 80, 10, True, "indoor"),  # sin lluvia ahora pero muy probable
        ("clear", 28, 5, 12, True, "beach"),
        ("clear", 28, 5, 50, True, "walk"),  # mucho viento
        ("cloudy", 28, 5, 10, True, "walk"),
        ("clear", 19, 0, 10, True, "walk"),
        ("clear", 28, 0, 10, False, "night"),  # de noche
        ("rain", 28, 90, 10, False, "indoor"),  # llueve de noche: bajo techo manda
    ],
)
def test_suggestion(icon, temp, rain, wind, is_day, expected):
    assert weather.build_suggestion(icon, temp, rain, wind, is_day) == expected


def test_every_weather_condition_is_a_known_key():
    from app.weather import _WMO

    assert {key for key, _ in _WMO.values()} <= {
        "clear", "mainly_clear", "partly_cloudy", "overcast", "fog", "light_drizzle", "drizzle",
        "heavy_drizzle", "freezing_drizzle", "light_rain", "rain", "heavy_rain", "freezing_rain",
        "light_snow", "snow", "heavy_snow", "snow_grains", "light_showers", "showers", "heavy_showers",
        "snow_showers", "thunderstorm", "thunderstorm_hail",
    }  # fmt: skip
