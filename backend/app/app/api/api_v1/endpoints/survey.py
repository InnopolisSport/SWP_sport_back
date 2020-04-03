from typing import Union

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.utils.db import get_db
from app.models.survey import SurveySubmission, TrainingTypes
from app.models.user import TokenUser
from app.api.utils.security import get_current_user

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

router = APIRouter()


@router.post("/{quiz_id}/submit")
def submit_survey(db=Depends(get_db), user: TokenUser = Depends(get_current_user), *,
                  quiz_id: int, submission: SurveySubmission):
    if not user.is_student():
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="Only students are allowed to fill the survey")

    # TODO: check that no answers were submitted previously

    if submission.training_type == TrainingTypes.IU_TRAINERS:
        if submission.priorities is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                detail="If IU trainers are chosen, list of priorities, must be set")
        elif len(set(submission.priorities)) != len(submission.priorities):
            raise HTTPException(status.HTTP_400_BAD_REQUEST,
                                detail=f"If IU trainers are chosen, list of priorities must contain unique values. "
                                       f"Got {submission.priorities}")

        else:
            pass
    else:
        pass

    raise HTTPException(status.HTTP_501_NOT_IMPLEMENTED, detail="The feature is under development")
