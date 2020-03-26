from django.db import models


class Attendance(models.Model):
    training = models.ForeignKey('Trainings', on_delete=models.CASCADE)
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    hours = models.DecimalField(max_digits=2, null=False, default=1)

    class Meta:
        db_table = "attendance"
        verbose_name_plural = "attendance"

    def __str__(self):
        return f"student {self.student.id} -> {self.training.id}"
