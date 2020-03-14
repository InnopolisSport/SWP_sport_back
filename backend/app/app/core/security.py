from passlib.context import CryptContext
from base64 import urlsafe_b64encode
from typing import Optional

from app.core.config import OAUTH_APP_ID, BASE_URL, OAUTH_SHARED_SECRET

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_code_retrieve_params(state: Optional[dict]) -> dict:
    return {
        "response_type": "code",
        "client_id": OAUTH_APP_ID,
        "redirect_uri": f"{BASE_URL}/get_code/get_code",
        "scope": "user_impersonation openid profile email allatclaims",
        "state": urlsafe_b64encode(str(state).encode())
    }


def get_token_retrieve_params(code: str) -> dict:
    return {
        "grant_type": "authorization_code",
        "code": code,
        "response_type": "code",

        "client_id": OAUTH_APP_ID,
        "client_secret": OAUTH_SHARED_SECRET,

        "redirect_uri": f"{BASE_URL}/get_code/get_code"
    }


def get_password_hash(password: str):
    return pwd_context.hash(password)
