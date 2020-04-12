from django.db import models


class Attendance(models.Model):
    training = models.ForeignKey('Training', on_delete=models.CASCADE)
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    hours = models.DecimalField(max_digits=3, decimal_places=2, default=1)

    class Meta:
        db_table = "attendance"
        verbose_name_plural = "attendance"

    def __str__(self):
        return f"{self.student} -> {self.training}, {self.hours} hours"
