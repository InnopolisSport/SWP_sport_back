from django.db import models


class Semester(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)

    class Meta:
        db_table = "semester"
        verbose_name_plural = "semesters"

    def __str__(self):
        return f"{self.name}"
