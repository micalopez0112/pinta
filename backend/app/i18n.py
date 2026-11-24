"""Idiomas de la API. El idioma se pide con `?lang=es|en|pt|de` y, si falta o no se
reconoce, se responde en español."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import Activity

SUPPORTED_LANGUAGES = ("es", "en", "pt", "de")
DEFAULT_LANGUAGE = "es"

# Campos de una actividad que se pueden traducir.
TRANSLATABLE_FIELDS = ("title", "description", "zone", "duration")


def normalize_language(value: str | None) -> str:
    """'EN', 'en-US' o 'pt-BR' -> 'en' / 'en' / 'pt'. Lo desconocido -> español."""
    if not value:
        return DEFAULT_LANGUAGE
    base = value.strip().lower()[:2]
    return base if base in SUPPORTED_LANGUAGES else DEFAULT_LANGUAGE


def localize_activity(activity: "Activity", language: str) -> dict:
    """La actividad como dict, con los textos en `language` (campo por campo: si falta
    una traducción se deja el texto en español)."""
    data = {
        "id": activity.id,
        "slug": activity.slug,
        "category": activity.category,
        "latitude": activity.latitude,
        "longitude": activity.longitude,
        "price_level": activity.price_level,
        "indoor": activity.indoor,
        **{field: getattr(activity, field) for field in TRANSLATABLE_FIELDS},
    }
    if language != DEFAULT_LANGUAGE:
        translation = (activity.translations or {}).get(language, {})
        for field in TRANSLATABLE_FIELDS:
            if translation.get(field):
                data[field] = translation[field]
    return data
