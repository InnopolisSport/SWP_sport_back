from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from sport.models import Group, SelfSportReport
from sport.signals.utils import update_attendance_record


@receiver(post_save, sender=SelfSportReport)
def update_hours_for_self_sport(
        sender,
        instance: SelfSportReport,
        created,
        **kwargs
):
    if created:
        return
    group = Group.objects.get(
        semester=instance.semester,
        name=settings.SELF_TRAINING_GROUP_NAME
    )
    training_custom_name = None
    if instance.training_type is not None:
        training_custom_name = f'[Self] {instance.training_type.name}'
    update_attendance_record(
        group=group,
        upload_date=instance.uploaded.date(),
        student=instance.student,
        hours=instance.hours,
        training_name=training_custom_name,
    )
