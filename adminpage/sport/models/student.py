from django.db import models


class Student(models.Model):
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    email = models.CharField(max_length=50, null=False, unique=True)

    class Meta:
        db_table = "student"
        verbose_name_plural = "students"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
