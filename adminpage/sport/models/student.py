from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver


class Student(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE,
        null=False,
        limit_choices_to={'groups__verbose_name': settings.STUDENT_GROUP_VERBOSE_NAME}
    )

    is_ill = models.BooleanField(default=False, null=False)

    class Meta:
        db_table = "student"
        verbose_name_plural = "students"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


@receiver(post_save, sender=User)
def save_student_profile(sender, instance, **kwargs):
    if Student.objects.filter(user=instance.pk).exists():
        instance.student.save()
