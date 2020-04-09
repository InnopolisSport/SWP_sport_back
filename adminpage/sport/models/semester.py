from datetime import datetime

from django.db import models


class Semester(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    start = models.DateTimeField(null=False, default=datetime.now)
    end = models.DateTimeField(null=False)
    choice_deadline = models.DateTimeField(null=False)

    class Meta:
        db_table = "semester"
        verbose_name_plural = "semesters"

    def __str__(self):
        return f"{self.name}"
