import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.utils.db import get_db

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()


@router.post("/")
def pong(db: Session = Depends(get_db)):
    return {"pong": True}


