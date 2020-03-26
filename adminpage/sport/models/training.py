from django.db import models


class Training(models.Model):
    class Weekdays(models.IntegerChoices):
        MONDAY = 0, "monday",
        TUESDAY = 1, "tuesday"
        WEDNESDAY = 2, "wednesday"
        THURSDAY = 3, "thursday"
        FRIDAY = 4, "friday"
        SATURDAY = 5, "saturday"
        SUNDAY = 6, "sunday"

    group = models.ForeignKey("Group", on_delete=models.CASCADE)
    weekday = models.IntegerField(choices=Weekdays.choices, null=False)
    start = models.TimeField(null=False)
    end = models.TimeField(null=False)

    class Meta:
        db_table = "training"
        verbose_name_plural = "trainings"

    def __str__(self):
        return f"{self.group.name}: {self.weekday}"
