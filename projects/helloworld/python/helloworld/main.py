"""FastAPI application entry point."""
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import api_router
from app.core.config import settings
from app.db.session import Base, get_engine

# Import models so they register with Base.metadata
from app import models  # noqa: F401


@asynccontextmanager
async def lifespan(_: FastAPI):
    """Create tables on startup.

    For production, prefer Alembic migrations; this keeps the demo simple.
    """
    Base.metadata.create_all(bind=get_engine())
    yield


def create_app() -> FastAPI:
    """Application factory."""
    app = FastAPI(
        title=settings.APP_NAME,
        debug=settings.DEBUG,
        lifespan=lifespan,
    )
    app.include_router(api_router, prefix=settings.API_V1_PREFIX)
    return app


app = create_app()
