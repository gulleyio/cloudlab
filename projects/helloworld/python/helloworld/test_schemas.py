"""Unit tests for Pydantic schemas."""
import pytest
from pydantic import ValidationError

from app.schemas.greeting import GreetingCreate, HelloResponse


class TestGreetingCreate:
    def test_valid_payload(self):
        schema = GreetingCreate(name="Alice")
        assert schema.name == "Alice"

    def test_rejects_empty_name(self):
        with pytest.raises(ValidationError):
            GreetingCreate(name="")

    def test_rejects_too_long_name(self):
        with pytest.raises(ValidationError):
            GreetingCreate(name="x" * 101)


class TestHelloResponse:
    def test_serialises_to_dict(self):
        response = HelloResponse(message="Hello, World!")
        assert response.model_dump() == {"message": "Hello, World!"}
