# FastAPI Hello World

A small but production-shaped FastAPI starter with PostgreSQL, layered architecture, and unit + integration tests.

## Project layout

```
app/
├── api/              # HTTP routes (thin)
├── core/             # Config (pydantic-settings)
├── db/               # SQLAlchemy engine, session, Base
├── models/           # ORM models
├── schemas/          # Pydantic request/response schemas
├── services/         # Business logic (no HTTP, no FastAPI)
└── main.py           # App factory + entry point
tests/
├── unit/             # Pure logic tests, no DB/HTTP
└── integration/      # Full-stack tests through TestClient + DB
```

The split between `api/`, `services/`, `schemas/`, and `models/` keeps HTTP concerns out of business logic and makes both layers independently testable.

## Quick start

```bash
# 1. Set up environment
cp .env.example .env
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt

# 2. Start Postgres (creates both helloworld and helloworld_test databases)
docker compose up -d

# 3. Run the app
uvicorn app.main:app --reload
```

Then open <http://localhost:8000/docs> for the interactive Swagger UI.

## Endpoints

| Method | Path                  | Description                         |
| ------ | --------------------- | ----------------------------------- |
| GET    | `/api/v1/health`      | Service + DB health check           |
| GET    | `/api/v1/hello`       | Stateless greeting (`?name=Alice`)  |
| POST   | `/api/v1/greetings`   | Create and persist a greeting       |
| GET    | `/api/v1/greetings`   | List recent greetings (newest first) |

## Running tests

By default tests use SQLite in-memory so the suite runs fast and doesn't need Postgres:

```bash
# All tests
pytest

# Unit tests only
pytest tests/unit

# Integration tests only
pytest tests/integration

# With coverage
pytest --cov=app --cov-report=term-missing
```

To run integration tests against a real Postgres instead (recommended in CI):

```bash
docker compose up -d
TEST_AGAINST_POSTGRES=1 pytest tests/integration
```

## Notes

- Tables are auto-created on app startup via the `lifespan` handler. For real projects, swap that for Alembic migrations — `alembic` is already in `requirements.txt`.
- The `get_db` dependency is overridden in tests via `app.dependency_overrides`, which is the canonical way to inject a test session into FastAPI.
- Each test runs inside a transaction that rolls back on teardown, so tests stay isolated without recreating the schema between them.
