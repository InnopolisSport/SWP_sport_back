from base64 import urlsafe_b64encode
from typing import Optional

from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.security.oauth2 import OAuth2, OAuthFlowsModel
from passlib.context import CryptContext
from starlette.status import HTTP_403_FORBIDDEN

from app.core.config import OAUTH_APP_ID, API_BASE_URL, OAUTH_SHARED_SECRET

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CookieAuth(OAuth2):
    def __init__(self, *, flows: OAuthFlowsModel = OAuthFlowsModel(), scheme_name: str = None, auto_error: bool = True):
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        authorization_header: str = request.headers.get("Authorization")
        authorization_cookie: str = request.cookies.get("access_token")
        if (not authorization_header) and (not authorization_cookie):
            if self.auto_error:
                raise HTTPException(
                    status_code=HTTP_403_FORBIDDEN, detail="Not authenticated"
                )
            else:
                return None
        return_token = authorization_header if authorization_header is not None else authorization_cookie
        if return_token.startswith("Bearer "):
            return_token = return_token[7:]
        return return_token


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_code_retrieve_params(state: Optional[dict]) -> dict:
    return {
        "response_type": "code",
        "client_id": OAUTH_APP_ID,
        "redirect_uri": f"{API_BASE_URL}/get_code/get_code",
        "scope": "user_impersonation openid profile email allatclaims user.read",
        "state": urlsafe_b64encode(str(state).encode())
    }


def get_token_retrieve_params(code: str) -> dict:
    return {
        "grant_type": "authorization_code",
        "code": code,
        "response_type": "code",

        "client_id": OAUTH_APP_ID,
        "client_secret": OAUTH_SHARED_SECRET,

        "redirect_uri": f"{API_BASE_URL}/get_code/get_code"
    }


def get_password_hash(password: str):
    return pwd_context.hash(password)
