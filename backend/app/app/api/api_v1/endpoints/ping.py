from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.utils.db import get_db
from app.models.user import User
from app.api.utils.security import get_current_user
from app.models.user import UserInDB
import app.crud

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()


@router.get("/")
def pong(db: Session = Depends(get_db)):
    return {"pong": True}

@router.get("/me", response_model=User)
def get_me(current_user: UserInDB = Depends(get_current_user)):
    logger.debug(f"in get_me, current_user type: {type(current_user)} - {current_user}")
    return current_user
