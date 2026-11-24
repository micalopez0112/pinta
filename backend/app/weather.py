"""Clima actual desde Open-Meteo (https://open-meteo.com): gratis y sin API key.

El frontend le pide el clima a nuestro backend y no a Open-Meteo directamente, así
guardamos la respuesta unos minutos (caché) y, si Open-Meteo falla, mostramos el último
dato que teníamos en vez de un error.
"""

import threading
import time

import httpx

from .config import settings

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"


class WeatherUnavailable(Exception):
    """No se pudo obtener el clima (y no hay nada guardado para mostrar)."""


# Código WMO de Open-Meteo -> (clave del estado del tiempo, tipo de ícono).
# La clave la traduce el frontend (weather.conditions.* en cada idioma): si se agrega
# una acá, hay que sumarla también en frontend/src/i18n/locales/.
_WMO = {
    0: ("clear", "clear"),
    1: ("mainly_clear", "clear"),
    2: ("partly_cloudy", "partly"),
    3: ("overcast", "cloudy"),
    45: ("fog", "fog"),
    48: ("fog", "fog"),
    51: ("light_drizzle", "rain"),
    53: ("drizzle", "rain"),
    55: ("heavy_drizzle", "rain"),
    56: ("freezing_drizzle", "rain"),
    57: ("freezing_drizzle", "rain"),
    61: ("light_rain", "rain"),
    63: ("rain", "rain"),
    65: ("heavy_rain", "rain"),
    66: ("freezing_rain", "rain"),
    67: ("freezing_rain", "rain"),
    71: ("light_snow", "snow"),
    73: ("snow", "snow"),
    75: ("heavy_snow", "snow"),
    77: ("snow_grains", "snow"),
    80: ("light_showers", "rain"),
    81: ("showers", "rain"),
    82: ("heavy_showers", "rain"),
    85: ("snow_showers", "snow"),
    86: ("snow_showers", "snow"),
    95: ("thunderstorm", "storm"),
    96: ("thunderstorm_hail", "storm"),
    99: ("thunderstorm_hail", "storm"),
}


def build_suggestion(icon: str, temperature: float, rain_probability: int | None, wind_kmh: float, is_day: bool) -> str:
    """El plan sugerido para el momento: "indoor", "night", "beach" o "walk"."""
    if icon in ("rain", "storm", "snow") or (rain_probability or 0) >= 60:
        return "indoor"
    if not is_day:
        return "night"
    if temperature >= 24 and wind_kmh < 35 and icon in ("clear", "partly"):
        return "beach"
    return "walk"


def parse_forecast(raw: dict) -> dict:
    """Convierte la respuesta de Open-Meteo en lo que necesita el frontend."""
    current = raw["current"]
    daily = raw["daily"]

    condition, icon = _WMO.get(current["weather_code"], ("unknown", "cloudy"))
    is_day = bool(current["is_day"])
    rain_probability = daily["precipitation_probability_max"][0]
    wind_kmh = current["wind_speed_10m"]
    temperature = current["temperature_2m"]
    sunset = daily["sunset"][0]

    return {
        "temperature": temperature,
        "feels_like": current["apparent_temperature"],
        "wind_kmh": wind_kmh,
        "is_day": is_day,
        "condition": condition,
        "icon": icon,
        "temp_max": daily["temperature_2m_max"][0],
        "temp_min": daily["temperature_2m_min"][0],
        "rain_probability": rain_probability,
        "uv_index_max": daily["uv_index_max"][0],
        "sunset": sunset[11:16] if sunset else None,  # "2026-11-23T19:31" -> "19:31"
        "observed_at": current["time"],
        "suggestion": build_suggestion(icon, temperature, rain_probability, wind_kmh, is_day),
    }


def fetch_forecast(latitude: float, longitude: float, timezone: str) -> dict:
    response = httpx.get(
        OPEN_METEO_URL,
        params={
            "latitude": latitude,
            "longitude": longitude,
            "current": "temperature_2m,apparent_temperature,is_day,weather_code,wind_speed_10m",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_probability_max,uv_index_max,sunset",
            "timezone": timezone,
            "forecast_days": 1,
        },
        timeout=8.0,
    )
    response.raise_for_status()
    return response.json()


_cache: dict[str, tuple[float, dict]] = {}
_lock = threading.Lock()


def get_weather(slug: str, latitude: float, longitude: float, timezone: str) -> dict:
    now = time.monotonic()
    with _lock:
        cached = _cache.get(slug)
    if cached and now - cached[0] < settings.weather_cache_seconds:
        return cached[1]

    try:
        weather = parse_forecast(fetch_forecast(latitude, longitude, timezone))
    except (httpx.HTTPError, KeyError, IndexError, TypeError, ValueError) as exc:
        if cached:
            return cached[1]  # dato viejo > ningún dato
        raise WeatherUnavailable(str(exc)) from exc

    with _lock:
        _cache[slug] = (now, weather)
    return weather
