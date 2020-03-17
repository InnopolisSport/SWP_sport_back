from fastapi import APIRouter

from app.api.api_v1.endpoints import login, users, ping  # ,items

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(ping.router, prefix="/ping", tags=["test"])
