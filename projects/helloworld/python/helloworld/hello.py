"""Hello endpoints — simple in-memory greetings, no DB."""
from fastapi import APIRouter, Query

from app.schemas.greeting import HelloResponse
from app.services.greeting_service import build_greeting_message

router = APIRouter(tags=["hello"])


@router.get("/hello", response_model=HelloResponse)
def hello(
    name: str = Query("World", min_length=1, max_length=100, description="Name to greet"),
) -> HelloResponse:
    """Return a hello-world style greeting for the given name."""
    return HelloResponse(message=build_greeting_message(name))
