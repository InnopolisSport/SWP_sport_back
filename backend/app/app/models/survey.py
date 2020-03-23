from enum import Enum
from typing import List, Set

from pydantic import Field, ConstrainedList

from .base import BaseModel
from app.core.config import PRIORITY_COUNT


class TrainingTypes(int, Enum):
    SPORT_CLUBS = 1
    IU_TRAINERS = 2
    SC_TRAINERS = 3


class SurveySubmission(BaseModel):
    training_type: TrainingTypes
    priorities: List[int] = Field(None, max_items=PRIORITY_COUNT, min_items=PRIORITY_COUNT)

