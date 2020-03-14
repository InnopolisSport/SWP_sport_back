from fastapi import APIRouter

from app.pages.endpoints import login

pages_router = APIRouter()
pages_router.include_router(login.router)
