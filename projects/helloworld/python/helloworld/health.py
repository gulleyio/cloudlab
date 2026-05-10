"""Health-check endpoint."""
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.greeting import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health(db: Session = Depends(get_db)) -> HealthResponse:
    """Return service + database status."""
    db_status = "ok"
    try:
        db.execute(text("SELECT 1"))
    except SQLAlchemyError:
        db_status = "error"
    return HealthResponse(status="ok", database=db_status)
