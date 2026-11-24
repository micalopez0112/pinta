"""Carga (o actualiza) los destinos y actividades iniciales.

    python -m app.seed            # carga o actualiza
    python -m app.seed --reset    # BORRA todas las tablas, las crea de nuevo y carga

Sin --reset se puede correr las veces que quieras: busca por `slug` y actualiza lo que ya
existe en vez de duplicar. No borra nada. (Usá --reset cuando cambie el esquema de la base,
por ejemplo si se agregó una columna: hoy no hay migraciones.)
"""

import argparse

from sqlalchemy import select
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session

from . import models
from .database import Base, SessionLocal, engine
from .seed_data import DESTINATIONS
from .seed_translations import TRANSLATIONS


def seed(db: Session) -> tuple[int, int]:
    destinations = activities = 0

    for data in DESTINATIONS:
        data = dict(data)
        activity_rows = data.pop("activities")

        destination = db.scalar(select(models.Destination).where(models.Destination.slug == data["slug"]))
        if destination is None:
            destination = models.Destination(**data)
            db.add(destination)
            db.flush()  # para tener destination.id
        else:
            for key, value in data.items():
                setattr(destination, key, value)
        destinations += 1

        for row in activity_rows:
            row = {**row, "translations": TRANSLATIONS.get(row["slug"], {})}
            activity = db.scalar(select(models.Activity).where(models.Activity.slug == row["slug"]))
            if activity is None:
                db.add(models.Activity(destination_id=destination.id, **row))
            else:
                for key, value in row.items():
                    setattr(activity, key, value)
                activity.destination_id = destination.id
            activities += 1

    db.commit()
    return destinations, activities


def describe_database(url: URL) -> str:
    """Servidor y nombre de la base, SIN usuario ni contraseña: "ep-abc.neon.tech/neondb"."""
    port = f":{url.port}" if url.port else ""
    return f"{url.host or url.drivername}{port}/{url.database or ''}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Carga las actividades iniciales.")
    parser.add_argument("--reset", action="store_true", help="borra y recrea las tablas antes de cargar")
    args = parser.parse_args()

    # Lo primero que se imprime es EN QUÉ base se va a trabajar: sin DATABASE_URL se usa la base
    # local de desarrollo, y esto evita creer que se cargó la de producción cuando no fue así.
    target = describe_database(engine.url)
    print(f"Base de datos: {target}")

    if args.reset:
        Base.metadata.drop_all(engine)
        print("Tablas borradas.")
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        destinations, activities = seed(db)
    print(f"Listo: {destinations} destino(s) y {activities} actividad(es) cargadas en {target}.")


if __name__ == "__main__":
    main()
