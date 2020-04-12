from functools import partial
from datetime import timedelta

from django.utils import timezone
from django.db import models


def now_offset(offset=0):
    return timezone.now() + timedelta(seconds=offset)


class Semester(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    start = models.DateTimeField(null=False, default=partial(now_offset, 0))
    end = models.DateTimeField(null=False, default=partial(now_offset, 2))
    choice_deadline = models.DateTimeField(null=False, default=partial(now_offset, 1))

    class Meta:
        db_table = "semester"
        verbose_name_plural = "semesters"

    def __str__(self):
        return f"{self.name}"
