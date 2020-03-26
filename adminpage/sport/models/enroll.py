from django.db import models


class Enroll(models.Model):
    student = models.ForeignKey("Student", primary_key=True, on_delete=models.CASCADE)
    group = models.ForeignKey("Group", primary_key=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "training"
        verbose_name_plural = "trainings"

    def __str__(self):
        return f"{self.group.name}: {self.student.email}"
