from django.db import models


class MeasurementSession(models.Model):
    student = models.ForeignKey(
        'Student',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    date = models.DateField(null=False)
    semester = models.ForeignKey(
        'Semester',
        on_delete=models.CASCADE,
        null=False,
        blank=False
    )
    approved = models.BooleanField(
        default=False
    )
