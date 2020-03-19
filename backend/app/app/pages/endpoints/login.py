from fastapi import APIRouter, Request
from app.pages.utils.jinja import templates

router = APIRouter()


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})
