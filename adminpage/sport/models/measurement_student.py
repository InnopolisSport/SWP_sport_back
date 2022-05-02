from django.db import models


class MeasurementStudent(models.Model):
    name = models.CharField(
        max_length=1000,
        null=True,
        blank=True
    )

    value_init = models.CharField(
        max_length=1000,
        null=True,
        blank=True
    )
