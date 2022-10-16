from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver

from sport.models import Group, SelfSportReport
from sport.signals.utils import create_attendance_record
from sport.utils import format_submission_html


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

    if not hasattr(instance, 'attendance'):
        instance.attendance = create_attendance_record(
            group=group,
            upload_date=instance.uploaded.date(),
            student=instance.student,
            hours=instance.hours,
            training_name=training_custom_name,
            cause_report=instance,
        )
    else:
        instance.attendance.hours = instance.hours
        instance.attendance.save()

    if instance.hours > 0:
        instance.student.notify_tg(
            '✅ *Преподаватель подтвердил прохождение тренировки!*\n\n'
            'Часы зачтены, можешь проверить в личном кабинете на сайте! 🎉\n\n'
            f'Дата: {instance.uploaded.date()}\n'
            f'Вид спорта: {instance.training_type.name}\n'
            f'Количество часов: {instance.hours}'
        )
    else:
        instance.attendance.delete()
        instance.student.notify_tg(
            '❌ *Преподаватель отказал в зачёте часов*\n\n'
            'Ознакомься с комментарием учителя 😢\n'
            f'Причина отказа: _{instance.comment}_\n\n'
            f'Дата: {instance.uploaded.date()}\n'
            f'Вид спорта: {instance.training_type.name}\n'
            f'Количество часов: {instance.hours}'
        )
