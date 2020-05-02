from django.db import models
from django.forms.utils import to_current_timezone


class Training(models.Model):
    group = models.ForeignKey("Group", on_delete=models.CASCADE)
    schedule = models.ForeignKey("Schedule", on_delete=models.SET_NULL, null=True, blank=True)
    start = models.DateTimeField(null=False)
    end = models.DateTimeField(null=False)

    class Meta:
        db_table = "training"
        verbose_name_plural = "trainings"
        constraints = [
            models.UniqueConstraint(fields=["group", "start", "end"], name="unique_training")
        ]

    def __str__(self):
        return f"{self.group} at {to_current_timezone(self.start).date()} " \
               f"{to_current_timezone(self.start).time().strftime('%H:%M')}-"\
               f"{to_current_timezone(self.end).time().strftime('%H:%M')}"
