"""Service layer: business logic separate from HTTP concerns.

Keeping logic here makes it easy to unit-test without spinning up FastAPI
or a database, and easy to reuse from other entry points (CLI, jobs, etc).
"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.greeting import Greeting


def build_greeting_message(name: str) -> str:
    """Pure function: returns a greeting string for the given name."""
    cleaned = name.strip()
    if not cleaned:
        raise ValueError("name must not be empty")
    return f"Hello, {cleaned}!"


def create_greeting(db: Session, name: str) -> Greeting:
    """Persist a new greeting and return it."""
    greeting = Greeting(
        name=name.strip(),
        message=build_greeting_message(name),
    )
    db.add(greeting)
    db.commit()
    db.refresh(greeting)
    return greeting


def list_greetings(db: Session, limit: int = 100) -> list[Greeting]:
    """Return the most recent greetings, newest first."""
    stmt = (
        select(Greeting)
        .order_by(Greeting.created_at.desc(), Greeting.id.desc())
        .limit(limit)
    )
    return list(db.scalars(stmt).all())
