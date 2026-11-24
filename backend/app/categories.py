"""Categorías de actividades: slug -> nombre en cada idioma. El orden es el de los filtros."""

from .i18n import DEFAULT_LANGUAGE

CATEGORIES: dict[str, dict[str, str]] = {
    "playa": {"es": "Playas", "en": "Beaches", "pt": "Praias", "de": "Strände"},
    "paseo": {"es": "Paseos", "en": "Walks", "pt": "Passeios", "de": "Spaziergänge"},
    "cultura": {"es": "Arte y cultura", "en": "Art & culture", "pt": "Arte e cultura", "de": "Kunst & Kultur"},
    "naturaleza": {"es": "Naturaleza", "en": "Nature", "pt": "Natureza", "de": "Natur"},
    "restaurante": {"es": "Restaurantes", "en": "Restaurants", "pt": "Restaurantes", "de": "Restaurants"},
    "supermercado": {"es": "Supermercados", "en": "Supermarkets", "pt": "Supermercados", "de": "Supermärkte"},
}


def category_label(slug: str, language: str) -> str:
    labels = CATEGORIES[slug]
    return labels.get(language) or labels[DEFAULT_LANGUAGE]
