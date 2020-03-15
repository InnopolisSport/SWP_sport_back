from fastapi import APIRouter

from app.pages.endpoints import login, main

pages_router = APIRouter()
pages_router.include_router(login.router)
pages_router.include_router(main.router)
