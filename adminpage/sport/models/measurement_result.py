from django.db import models


class MeasurementResult(models.Model):
    session = models.ForeignKey(
        'MeasurementSession',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    measurement = models.ForeignKey(
        'MeasurementStudent',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )

    value = models.IntegerField()
