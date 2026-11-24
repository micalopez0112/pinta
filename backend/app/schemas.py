from pydantic import BaseModel, ConfigDict


class DestinationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    slug: str
    name: str
    country: str
    latitude: float
    longitude: float


class ActivityOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    slug: str
    title: str
    category: str
    description: str
    zone: str
    latitude: float
    longitude: float
    price_level: int | None
    duration: str | None
    indoor: bool


class CategoryOut(BaseModel):
    slug: str
    label: str


class WeatherOut(BaseModel):
    """El clima va con claves (no con texto): el frontend las traduce al idioma elegido."""

    temperature: float
    feels_like: float
    wind_kmh: float
    is_day: bool
    # Clave del estado del tiempo: "clear", "overcast", "light_rain", "thunderstorm"…
    # (la lista completa está en weather.py)
    condition: str
    # "clear" | "partly" | "cloudy" | "fog" | "rain" | "storm" | "snow"
    icon: str
    temp_max: float
    temp_min: float
    rain_probability: int | None
    uv_index_max: float | None
    sunset: str | None
    observed_at: str
    # Plan sugerido para hoy: "indoor" | "night" | "beach" | "walk"
    suggestion: str
