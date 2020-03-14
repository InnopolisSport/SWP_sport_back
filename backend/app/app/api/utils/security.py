import jwt
from fastapi import Depends, HTTPException, Security
from fastapi.security import (
    OAuth2PasswordBearer, OAuth2AuthorizationCodeBearer, OAuth2
    # SecurityScopes
)
from fastapi.security.oauth2 import OAuthFlowsModel
from jwt import PyJWTError
from sqlalchemy.orm import Session
from starlette.status import HTTP_403_FORBIDDEN

from app import crud
from app.api.utils.db import get_db
from app.core import config
from app.core.jwt import ALGORITHM
from app.db_models.user import User
from app.models.token import TokenPayload

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# reusable_oauth2 = OAuth2PasswordBearer(
#     tokenUrl="/api/login/access-token",
# scopes={"me": "Read information about the current user.", "items": "Read items."},
# )

reusable_oauth2 = OAuth2(
    flows=OAuthFlowsModel(
        implicit={
            "authorizationUrl": f"{config.BASE_URL}/login/test"
            # "authorizationUrl": "https://sso.university.innopolis.ru/adfs/oauth2/authorize"
        }
    )
)


def get_current_user(
        db: Session = Depends(get_db), token: str = Security(reusable_oauth2)
):
    try:
        logger.debug(token)
        # payload = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])
        payload = jwt.get_unverified_header(token)
        token_data = TokenPayload(**payload)
    except PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    user = crud.user.get(db, user_id=token_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(current_user: User = Security(get_current_user)):
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_superuser(current_user: User = Security(get_current_user)):
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
