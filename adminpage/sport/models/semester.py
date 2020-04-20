from datetime import timedelta, date

from django.db import models
from django.utils import timezone


def now_offset(offset=0):
    return timezone.now() + timedelta(seconds=offset)


def today() -> date:
    return timezone.now().date()


class Semester(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    start = models.DateField(null=False, default=today)
    end = models.DateField(null=False, default=today)
    choice_deadline = models.DateField(null=False, default=today)

    class Meta:
        db_table = "semester"
        verbose_name_plural = "semesters"

    def __str__(self):
        return f"{self.name}"
