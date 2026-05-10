"""Aggregate API routers."""
from fastapi import APIRouter

from app.api import greetings, health, hello

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(hello.router)
api_router.include_router(greetings.router)
