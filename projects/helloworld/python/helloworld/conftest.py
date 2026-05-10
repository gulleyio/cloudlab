"""Shared pytest fixtures.

We use SQLite in-memory for tests by default so the suite runs without a
running Postgres. To run integration tests against real Postgres instead,
set TEST_AGAINST_POSTGRES=1 in the environment and ensure TEST_POSTGRES_DB
exists.
"""
import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.db import session as db_session_module
from app.db.session import Base, get_db


def _build_test_engine():
    if os.getenv("TEST_AGAINST_POSTGRES") == "1":
        return create_engine(settings.TEST_DATABASE_URL, pool_pre_ping=True)
    # SQLite in-memory, shared across the connection pool for the test session
    return create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )


@pytest.fixture(scope="session")
def engine():
    """Test database engine; tables created once per session.

    We also override ``get_engine`` so the app's lifespan startup hook
    uses the test engine instead of trying to connect to real Postgres.
    """
    eng = _build_test_engine()
    db_session_module.get_engine.cache_clear()
    db_session_module.get_engine = lambda: eng  # type: ignore[assignment]
    Base.metadata.create_all(bind=eng)
    yield eng
    Base.metadata.drop_all(bind=eng)
    eng.dispose()


@pytest.fixture
def db_session(engine) -> Generator[Session, None, None]:
    """Function-scoped DB session that rolls back after each test.

    Wrapping each test in a transaction keeps tests isolated from each
    other without paying to recreate the schema between tests.
    """
    connection = engine.connect()
    transaction = connection.begin()
    TestSession = sessionmaker(bind=connection, expire_on_commit=False)
    session = TestSession()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session) -> Generator[TestClient, None, None]:
    """TestClient with the DB dependency overridden to the test session."""
    # Import inside the fixture so the engine override above is in effect first
    from app.main import create_app

    app = create_app()

    def override_get_db() -> Generator[Session, None, None]:
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
