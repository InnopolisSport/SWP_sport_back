import logging

from fastapi import APIRouter, HTTPException
from starlette.responses import JSONResponse, HTMLResponse
from starlette.status import HTTP_403_FORBIDDEN

from app.core.config import FAKE_LOGIN
from app.core.jwt import create_access_token
from app.models.token import Token
from app.models.user import TokenUser

router = APIRouter()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@router.post("/setcookie", response_model=Token)
def set_cookie(user_data: TokenUser):
    if not FAKE_LOGIN:
        raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="You can't use fake login on production")

    access_token = create_access_token(data={
        "given_name": user_data.first_name,
        "family_name": user_data.last_name,
        "email": user_data.email,
        "group": user_data.groups,
        "role": user_data.role
    })

    response = JSONResponse(content={"access_token": access_token, "token_type": "bearer"})
    response.set_cookie(key="access_token", value=access_token)
    # response.set_cookie(key="id_token", value=id_token)
    return response


@router.get("/clearcookie")
def clear_cookie():
    response = HTMLResponse(status_code=200, content="Login cookies were cleared")
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="id_token")
    return response
