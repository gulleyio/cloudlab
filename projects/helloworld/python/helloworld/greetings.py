"""Greetings endpoints — persist greetings in PostgreSQL."""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.greeting import GreetingCreate, GreetingRead
from app.services import greeting_service

router = APIRouter(prefix="/greetings", tags=["greetings"])


@router.post(
    "",
    response_model=GreetingRead,
    status_code=status.HTTP_201_CREATED,
    summary="Create a greeting",
)
def create_greeting(
    payload: GreetingCreate,
    db: Session = Depends(get_db),
) -> GreetingRead:
    """Create and persist a new greeting."""
    greeting = greeting_service.create_greeting(db, name=payload.name)
    return GreetingRead.model_validate(greeting)


@router.get(
    "",
    response_model=list[GreetingRead],
    summary="List recent greetings",
)
def list_greetings(
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
) -> list[GreetingRead]:
    """Return recent greetings, newest first."""
    greetings = greeting_service.list_greetings(db, limit=limit)
    return [GreetingRead.model_validate(g) for g in greetings]
