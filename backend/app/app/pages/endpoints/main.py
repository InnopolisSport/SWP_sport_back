import logging

from fastapi import APIRouter, Depends, responses

from app.utils.security import get_current_user_optional

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()


@router.get("/")
def index_page(
        current_user: dict = Depends(get_current_user_optional)
):
    if current_user:
        return responses.RedirectResponse(url='/profile')
    else:
        return responses.RedirectResponse(url='/login')
