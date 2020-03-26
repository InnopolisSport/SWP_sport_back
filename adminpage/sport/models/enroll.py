from django.db import models


class Enroll(models.Model):
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    group = models.ForeignKey("Group", on_delete=models.CASCADE)

    class Meta:
        db_table = "enroll"
        verbose_name_plural = "enrolls"
        unique_together = (("student", "group"),)

    def __str__(self):
        return f"{self.group.name}: {self.student.email}"
