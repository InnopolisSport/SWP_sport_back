import logging
from typing import Optional

import jwt
from fastapi import HTTPException, Security, Cookie
from fastapi.openapi.models import OAuthFlowImplicit
from fastapi.security.oauth2 import OAuthFlowsModel
from jwt import PyJWTError
from starlette.status import HTTP_401_UNAUTHORIZED

from app.core import config
from app.core.jwt import ALGORITHM
from app.core.security import CookieAuth
from app.models.user import TokenUser

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

reusable_oauth2 = CookieAuth(
    flows=OAuthFlowsModel(
        implicit=OAuthFlowImplicit(
            authorizationUrl=f"{config.API_BASE_URL}/login"
        )
    ),
    auto_error=False
)


def process_token(token) -> TokenUser:
    # logger.debug(f"Access: {token}\n\n")
    try:
        # TODO: ask IT dep for verification URL
        access_payload = jwt.decode(token, verify=False, algorithms=[ALGORITHM])
        # id_payload = jwt.decode(id_token, verify=False, algorithms=[ALGORITHM])
    except PyJWTError as e:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials: {e}"
        )
    return TokenUser(
        first_name=access_payload["given_name"],
        last_name=access_payload["family_name"],
        email=access_payload["email"],
        groups=access_payload["group"],
        role=access_payload.get("role", None)
    )


def get_current_user(
        token: str = Security(reusable_oauth2),
        access_token=Cookie(None),  # needs for documentation, anyway cookie token is retrieved by oauth
) -> TokenUser:
    if token is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED, detail="Not authenticated"
        )
    return process_token(token)


def get_current_user_optional(
        token: str = Security(reusable_oauth2),
        access_token=Cookie(None),  # needs for documentation, anyway cookie token is retrieved by oauth
) -> Optional[TokenUser]:
    # TODO Ask IT dep for identification endpoint
    if token is None:
        return None
    return process_token(token)

