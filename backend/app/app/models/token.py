from .base import Base


class TokenRetrieval(Base):
    access_token: str
    token_type: str
    expires_in: int
    resource: str
    refresh_token: str
    refresh_token_expires_in: int
    scope: str
    id_token: str


class Token(Base):
    access_token: str
    token_type: str


class TokenPayload(Base):
    user_id: int = None
