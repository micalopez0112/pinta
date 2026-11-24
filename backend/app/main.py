from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models  # noqa: F401  (importarlo registra las tablas en Base)
from .api import router
from .config import settings
from .database import Base, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Versión 1: creamos las tablas si no existen. Cuando el esquema empiece a cambiar
    # (por ejemplo, al sumar usuarios) conviene pasar a migraciones con Alembic.
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="Pinta API", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_methods=["GET"],  # cuando haya registro de usuarios, sumar POST
    allow_headers=["*"],
)

app.include_router(router)
