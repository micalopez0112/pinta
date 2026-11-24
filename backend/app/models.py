from datetime import datetime

from sqlalchemy import JSON, Boolean, DateTime, Float, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class Destination(Base):
    """Un lugar con actividades (hoy solo Punta del Este, mañana más)."""

    __tablename__ = "destinations"

    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(120))
    country: Mapped[str] = mapped_column(String(80))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    timezone: Mapped[str] = mapped_column(String(64), default="America/Montevideo")

    activities: Mapped[list["Activity"]] = relationship(
        back_populates="destination", cascade="all, delete-orphan"
    )


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    destination_id: Mapped[int] = mapped_column(ForeignKey("destinations.id"), index=True)
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(160))
    category: Mapped[str] = mapped_column(String(40), index=True)
    description: Mapped[str] = mapped_column(Text)
    zone: Mapped[str] = mapped_column(String(120))
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    # 0 = gratis, 1 a 3 = de más barato a más caro, NULL = "consultar".
    price_level: Mapped[int | None] = mapped_column(Integer, nullable=True)
    duration: Mapped[str | None] = mapped_column(String(60), nullable=True)
    # True si se puede hacer bajo techo (útil para días de lluvia).
    indoor: Mapped[bool] = mapped_column(Boolean, default=False)
    # Los textos de arriba (title, description, zone, duration) están en español, el idioma por
    # defecto. Las traducciones van acá, por idioma:
    #   {"en": {"title": "...", "description": "...", "zone": "...", "duration": "..."}, "de": {...}}
    # Lo que falte en un idioma se muestra en español.
    translations: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    destination: Mapped[Destination] = relationship(back_populates="activities")
