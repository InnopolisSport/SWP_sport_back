from django.db import models


class SelfSportType(models.Model):
    name = models.CharField(
        max_length=50,
        null=False,
        unique=True,
    )

    application_rule = models.TextField()

    is_active = models.BooleanField(
        default=True
    )

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.__repr__()

    class Meta:
        db_table = "self_sport_group"
        permissions = [
            ("more_than_10_hours_of_self_sport", "Can have more then 10 hours of self sport"),
        ]
