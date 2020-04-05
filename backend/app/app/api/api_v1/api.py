from fastapi import APIRouter

#
from app.api.api_v1.endpoints import login, fake_login, survey, calendar, enroll, ping  # ,items

#
api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(fake_login.router, prefix="/fake_login", tags=["fake-login"])
api_router.include_router(survey.router, tags=['survey'], prefix="/survey")
api_router.include_router(calendar.router, tags=["calendar"], prefix="/calendar")
api_router.include_router(enroll.router, tags=["enrollment"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# # api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(ping.router, prefix="/ping", tags=["test"])
