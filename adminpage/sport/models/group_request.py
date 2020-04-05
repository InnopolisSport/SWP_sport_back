from django.db import models


class GroupRequest(models.Model):
    class Statuses(models.IntegerChoices):
        OPEN = 0, "open"
        ACCEPTED = 1, "accepted"
        REJECTED = 2, "rejected"

    class Types(models.IntegerChoices):
        GROUP_ENROLL = 0, "enroll to a group"
        GROUP_LEAVE = 1, "leave a group"

    group = models.ForeignKey("Group", on_delete=models.CASCADE)
    student = models.ForeignKey("Student", on_delete=models.CASCADE)
    created = models.DateTimeField(null=False, auto_now_add=True)
    last_update = models.DateTimeField(null=False, auto_now=True)
    status = models.IntegerField(choices=Statuses.choices, default=Statuses.OPEN, null=False)
    type = models.IntegerField(choices=Types.choices, null=False)

    class Meta:
        db_table = "group_request"
        verbose_name_plural = "group requests"

    def __str__(self):
        return f"{self.student.email}"
