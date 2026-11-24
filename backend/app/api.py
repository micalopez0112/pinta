from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from . import weather
from .categories import CATEGORIES, category_label
from .database import get_db
from .i18n import localize_activity, normalize_language
from .models import Activity, Destination
from .schemas import ActivityOut, CategoryOut, DestinationOut, WeatherOut

router = APIRouter(prefix="/api")

# ?lang=es|en|pt|de. Si falta o no se reconoce, se responde en español.
Lang = Annotated[
    str | None,
    Query(description="Idioma de los textos: es, en, pt o de (por defecto, es)."),
]


def _get_destination(db: Session, slug: str) -> Destination:
    destination = db.scalar(select(Destination).where(Destination.slug == slug))
    if destination is None:
        raise HTTPException(status_code=404, detail="Destino no encontrado")
    return destination


@router.get("/ping")
def ping() -> dict:
    """"¿La API está viva?" SIN tocar la base de datos. Es la que conviene usar para los chequeos
    de salud del hosting y para mantener la API despierta: la base gratis (Neon) se apaga sola
    cuando no se usa, y /api/health la despertaría en cada chequeo, gastando el cupo del mes."""
    return {"status": "ok"}


@router.get("/health")
def health(db: Session = Depends(get_db)) -> dict:
    db.execute(text("SELECT 1"))
    return {"status": "ok"}


@router.get("/categories", response_model=list[CategoryOut])
def list_categories(lang: Lang = None) -> list[dict]:
    language = normalize_language(lang)
    return [{"slug": slug, "label": category_label(slug, language)} for slug in CATEGORIES]


@router.get("/destinations", response_model=list[DestinationOut])
def list_destinations(db: Session = Depends(get_db)):
    return db.scalars(select(Destination).order_by(Destination.name)).all()


@router.get("/destinations/{slug}", response_model=DestinationOut)
def get_destination(slug: str, db: Session = Depends(get_db)):
    return _get_destination(db, slug)


@router.get("/destinations/{slug}/activities", response_model=list[ActivityOut])
def list_activities(
    slug: str,
    category: str | None = None,
    indoor: bool | None = None,
    lang: Lang = None,
    db: Session = Depends(get_db),
):
    destination = _get_destination(db, slug)
    query = select(Activity).where(Activity.destination_id == destination.id)
    if category:
        query = query.where(Activity.category == category)
    if indoor is not None:
        query = query.where(Activity.indoor == indoor)
    # Orden de carga: el de seed_data.py, donde las imperdibles van primero.
    activities = db.scalars(query.order_by(Activity.id)).all()
    language = normalize_language(lang)
    return [localize_activity(activity, language) for activity in activities]


@router.get("/destinations/{slug}/weather", response_model=WeatherOut)
def get_weather(slug: str, db: Session = Depends(get_db)):
    destination = _get_destination(db, slug)
    try:
        return weather.get_weather(
            destination.slug, destination.latitude, destination.longitude, destination.timezone
        )
    except weather.WeatherUnavailable:
        raise HTTPException(status_code=502, detail="No pudimos obtener el clima en este momento")
