from fastapi import APIRouter

from app.pages.endpoints import login, main

pages_router = APIRouter()
pages_router.include_router(login.router, tags=["pages"])
pages_router.include_router(main.router, tags=["pages"])
