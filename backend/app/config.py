from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración. Se puede pisar con variables de entorno o con un archivo .env."""

    # En producción es la cadena de conexión que entrega el servicio de base de datos (Neon,
    # etc.): se acepta tal cual, con "postgresql://" o "postgres://" (ver más abajo).
    database_url: str = "postgresql+psycopg://pinta:pinta@localhost:5434/pinta"
    # Orígenes permitidos por CORS, separados por coma.
    cors_origins: str = "http://localhost:5173"
    # Cuánto tiempo (segundos) reutilizamos la respuesta del clima.
    weather_cache_seconds: int = 600

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @field_validator("database_url")
    @classmethod
    def use_psycopg_driver(cls, value: str) -> str:
        """Neon, Render y otros entregan "postgresql://..." (o "postgres://..."), y SQLAlchemy
        necesita saber qué driver usar: "postgresql+psycopg://..."."""
        for prefix in ("postgres://", "postgresql://"):
            if value.startswith(prefix):
                return "postgresql+psycopg://" + value[len(prefix) :]
        return value

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]


settings = Settings()
