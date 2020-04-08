import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()


@router.post("/")
def pong():
    return {"pong": True}
