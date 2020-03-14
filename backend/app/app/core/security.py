from passlib.context import CryptContext
from base64 import urlsafe_b64encode
from typing import Optional

from app.core.config import OAUTH_APP_ID, BASE_URL

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_auth_url():
    pass


def get_auth_params(state: Optional[str]) -> dict:
    return {
        'response_type': 'code',
        'client_id': OAUTH_APP_ID,
        'redirect_uri': BASE_URL + 'get_code',
        'scope': 'user_impersonation openid profile email allatclaims',
        'state': urlsafe_b64encode(str(state).encode())
    }


def get_password_hash(password: str):
    return pwd_context.hash(password)
