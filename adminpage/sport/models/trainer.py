from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Trainer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        null=False,
        limit_choices_to={'groups__verbose_name': settings.TRAINER_GROUP_VERBOSE_NAME}
    )

    class Meta:
        db_table = "trainer"
        verbose_name_plural = "trainers"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
