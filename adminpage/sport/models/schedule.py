from django.db import models


class Schedule(models.Model):
    class Weekday(models.IntegerChoices):
        MONDAY = 0, "Monday"
        TUESDAY = 1, "Tuesday"
        WEDNESDAY = 2, "Wednesday"
        THURSDAY = 3, "Thursday"
        FRIDAY = 4, "Friday"
        SATURDAY = 5, "Saturday"
        SUNDAY = 7, "Sunday"

    group = models.ForeignKey('Group', on_delete=models.CASCADE, null=False)
    weekday = models.IntegerField(choices=Weekday.choices, null=False)
    start = models.TimeField(auto_now=False, auto_now_add=False, null=False)
    end = models.TimeField(auto_now=False, auto_now_add=False, null=False)

    class Meta:
        db_table = "schedule"
        verbose_name = "schedule timeslot"
        verbose_name_plural = "schedule timeslots"

    def __str__(self):
        return f"{self.group} {self.weekday} {self.start}-{self.end}"
