from django.db import models


class MedicalGroups(models.IntegerChoices):
    """
    NO_CHECKUP, SPECIAL2 - can't attend any trainings
    SPECIAL1 - can attend special groups
    PREPARATIVE, GENERAL - can attend everything
    """
    NO_CHECKUP = -2, "Medical checkup not passed"
    SPECIAL2 = -1, "Special 2"
    SPECIAL1 = 0, "Special 1"
    PREPARATIVE = 1, "Preparative"
    GENERAL = 2, "General"


class StudentStatuses(models.IntegerChoices):
    NORMAL = 0, "normal"
    DROPPED = 1, "dropped"
    ACADEMIC_LEAVE = 2, "academic leave"
    ALUMNI = 3, "alumni"
