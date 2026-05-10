from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter()


@router.get("/hello")
def get_hello(name: str):
    return f"Hello + {name}"


@router.post("/add/name")
def post_hello(name: str):
    return f"Hello + {name}"
