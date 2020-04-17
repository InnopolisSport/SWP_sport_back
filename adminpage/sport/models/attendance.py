from django.core.exceptions import ValidationError
from django.db import models


def validate_hours(hours):
    if hours <= 0:
        raise ValidationError('Only positive values are allowed')


class Attendance(models.Model):
    training = models.ForeignKey('Training', on_delete=models.SET_NULL, null=True)
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    hours = models.DecimalField(max_digits=3, decimal_places=2, default=1, validators=[validate_hours])

    class Meta:
        db_table = "attendance"
        verbose_name_plural = "attendance"

    def __str__(self):
        return f"{self.student} -> {self.training}, {self.hours} hours"
