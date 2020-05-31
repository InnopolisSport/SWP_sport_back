from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.conf import settings


class Trainer(models.Model):
    # TODO: remove in future
    # this 3 fields are used for back-compatibility. 
    # In Django they are stored in user account
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50, null=True, unique=True)

    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        null=True, # for back compatibility. Make False in future
        limit_choices_to={'groups__verbose_name': settings.TRAINER_GROUP_VERBOSE_NAME}
        )

    class Meta:
        db_table = "trainer"
        verbose_name_plural = "trainers"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

