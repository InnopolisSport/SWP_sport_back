from django.utils import timezone
from django.db import models


class Semester(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    start = models.DateTimeField(null=False, default=timezone.now)
    end = models.DateTimeField(null=False, default=timezone.now)
    choice_deadline = models.DateTimeField(null=False, default=timezone.now)

    class Meta:
        db_table = "semester"
        verbose_name_plural = "semesters"

    def __str__(self):
        return f"{self.name}"
