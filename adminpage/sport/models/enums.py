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


medical_groups_description = {
    MedicalGroups.NO_CHECKUP: "You can't get sport hours "
                              "for training unless "
                              "you pass a checkup",
    MedicalGroups.SPECIAL2: "You can't attend trainings "
                            "instead you should write a "
                            "report on sport related topic",
    MedicalGroups.SPECIAL1: "You can attend only special groups. "
                            "That is why you might see less available groups "
                            "than your classmates",
    **dict.fromkeys(
        [MedicalGroups.PREPARATIVE, MedicalGroups.General], "Your health status is considered to be OK. "
                                                            "You can attend any trainings"
    )
}
