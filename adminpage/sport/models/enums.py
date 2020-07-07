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
    General = 2, "General"


medical_groups_name = {}
medical_groups_description = {}
