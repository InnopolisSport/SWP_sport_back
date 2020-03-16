import logging
from ast import literal_eval
from base64 import urlsafe_b64decode
from datetime import timedelta
from urllib.parse import urlencode

import requests
from fastapi import APIRouter, Depends, HTTPException, responses, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import crud
from app.api.utils.db import get_db
from app.api.utils.link import form_link
from app.api.utils.security import get_current_user
from app.core import config
from app.core.jwt import create_access_token
from app.core.security import get_code_retrieve_params, get_token_retrieve_params
from app.models.token import Token, TokenRetrieval

router = APIRouter()

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


@router.post("/login/access-token", response_model=Token, tags=["login"], deprecated=True)
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


@router.post("/login/test-token", tags=["login"])
def test_token(current_user: dict = Depends(get_current_user)):
    """
    Test access token
    """
    return current_user


@router.get("/loginform", tags=["login"])
def login_from_form():
    return responses.RedirectResponse(
        url="/api/login?state=login&redirect_uri=https%3A%2F%2Fhelpdesk.innopolis.university"
    )


@router.get("/login", tags=["login"], response_class=responses.HTMLResponse)
def loginSSO(state: str, redirect_uri: str):
    params = get_code_retrieve_params({"state": state, "redirect_uri": redirect_uri})
    auth_url = f"{config.OAUTH_AUTHORIZATION_BASE_URL}?{urlencode(params)}"
    return responses.RedirectResponse(url=auth_url)


@router.get("/get_code/get_code")
def process_code(code: str, state: str, client_request_id: str = Query(..., alias="client-request-id"),
                 # * , response: Response
                 ):
    state = literal_eval(urlsafe_b64decode(state.encode()).decode())
    if not state["redirect_uri"].startswith(config.BASE_URL):
        raise HTTPException(status_code=400,
                            detail=f"Redirect uri must start with {config.BASE_URL} Got {state['redirect_uri']}")

    params = get_token_retrieve_params(code)
    resp = requests.post(config.OAUTH_TOKEN_URL, data=params, headers={
        'content-type': 'application/json'
    })

    data = resp.json()

    if data.get("error", None):
        raise HTTPException(status_code=401, detail=data)
    else:
        tokens = TokenRetrieval(**data)
        if state["redirect_uri"].startswith(config.DOCS_BASE_URL):
            url = form_link(state["redirect_uri"],
                            {
                                "state": state["state"],
                                "access_token": tokens.access_token,
                                "expires_in": tokens.expires_in,
                            }
                            )
        else:
            url = form_link(state["redirect_uri"],
                            {
                                "state": state["state"]
                            }
                            )
    response = responses.RedirectResponse(
        url=url,
        status_code=302
    )
    response.set_cookie(key="access_token", value=f"Bearer {tokens.access_token}", expires=tokens.expires_in)
    response.set_cookie(key="id_token", value=f"{tokens.id_token}", expires=tokens.expires_in)
    response.set_cookie(key="refresh_token", value=f"{tokens.refresh_token}",
                        expires=tokens.refresh_token_expires_in)

    return response
