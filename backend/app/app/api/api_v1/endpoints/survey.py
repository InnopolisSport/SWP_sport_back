from fastapi import APIRouter, Depends

from app.api.utils.db import get_db
from app.models.user import User
from app.api.utils.security import get_current_user
from app.models.user import UserInDB
import app.crud

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()

