from django.db import models


class Training(models.Model):
    group = models.ForeignKey("Group", on_delete=models.CASCADE)
    start = models.DateTimeField(null=False)
    end = models.DateTimeField(null=False)

    class Meta:
        db_table = "training"
        verbose_name_plural = "trainings"

    def __str__(self):
        return f"{self.group} at {self.start.date()} " \
               f"{self.start.time().strftime('%H:%M')}-{self.end.time().strftime('%H:%M')}"
