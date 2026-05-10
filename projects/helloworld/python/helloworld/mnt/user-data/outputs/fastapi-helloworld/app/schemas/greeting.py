"""Pydantic schemas for request/response validation."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class GreetingBase(BaseModel):
    """Shared fields for greeting schemas."""

    name: str = Field(..., min_length=1, max_length=100, description="Name to greet")


class GreetingCreate(GreetingBase):
    """Schema for creating a greeting."""


class GreetingRead(GreetingBase):
    """Schema returned to clients."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    message: str
    created_at: datetime


class HelloResponse(BaseModel):
    """Simple hello response (no DB)."""

    message: str = Field(..., examples=["Hello, World!"])


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., examples=["ok"])
    database: str = Field(..., examples=["ok"])
