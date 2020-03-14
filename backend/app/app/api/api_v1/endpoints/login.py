from datetime import timedelta

from fastapi import APIRouter, Body, Depends, HTTPException, responses
from fastapi.security import OAuth2PasswordRequestForm
from urllib.parse import urlencode
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.api.utils.security import get_current_user
from app.core import config
from app.core.jwt import create_access_token
from app.core.security import get_password_hash, get_auth_params
from app.db_models.user import User as DBUser
from app.models.token import Token
from app.models.user import User

router = APIRouter()


@router.post("/login/access-token", response_model=Token, tags=["login"])
def login_access_token(
        db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"user_id": user.id}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/login/test-token", tags=["login"], response_model=User)
def test_token(current_user: DBUser = Depends(get_current_user)):
    """
    Test access token
    """
    return current_user


@router.get("/login/test", tags=["login"], response_class=responses.HTMLResponse)
def loginSSO():
    params = get_auth_params(None)
    auth_url = f"{config.OAUTH_AUTHORIZATION_BASE_URL}?{urlencode(params)}"
    return f"<a href={auth_url}>Залогиниться</a>\n" \
           f"<br>\n" \
           f"<a href={config.OAUTH_END_SESSION_ENDPOINT}>Выйти из системы</a>"
