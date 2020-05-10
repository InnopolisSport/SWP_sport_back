import logging

from fastapi import APIRouter, Depends, Path, status, responses

from app.db import find_student, get_attended_training_info
from app.models.user import TokenUser
from app.utils.db import get_db
from app.utils.security import get_current_user

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()


@router.get("/{training_id}")
def toggle_sick(db=Depends(get_db), *, user: TokenUser = Depends(get_current_user), training_id: int = Path(..., gt=0)):
    if not user.is_student():
        return responses.JSONResponse(status_code=status.HTTP_200_OK, content={
            "ok": False,
            "error": {
                "description": "Not a student account",
                "code": 3,
            }
        })

    student_id = find_student(db, user.email).id
    info = get_attended_training_info(db, training_id, student_id)
    return info
