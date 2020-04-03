from fastapi import APIRouter

from app.pages.endpoints import login, main, survey, profile, calendar

pages_router = APIRouter()
pages_router.include_router(login.router, tags=["pages"])
pages_router.include_router(main.router, tags=["pages"])
pages_router.include_router(survey.router, tags=["pages"])
pages_router.include_router(profile.router, tags=["pages"])
pages_router.include_router(calendar.router, tags=["pages"])
