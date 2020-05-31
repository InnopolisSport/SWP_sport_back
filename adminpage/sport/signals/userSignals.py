from django.conf import settings
from django.contrib.auth.models import User, Group
from django.db.models.signals import m2m_changed
from django.dispatch.dispatcher import receiver

from sport.models import Student, Trainer


def get_current_group_mapping():
    group_mapping = {}
    user_groups = Group.objects.filter(
        verbose_name__in=[
            settings.STUDENT_GROUP_VERBOSE_NAME,
            settings.TRAINER_GROUP_VERBOSE_NAME,
        ],
    ).all()

    for group in user_groups:
        group_mapping.update({group.verbose_name: group.pk})

    return group_mapping


@receiver(
    m2m_changed,
    sender=User.groups.through
)
# if user is add to a group, this will create a corresponding profile
def create_student_profile(instance, action, reverse, pk_set, **kwargs):
    if not reverse:
        group_mapping = get_current_group_mapping()
        if group_mapping.get(settings.STUDENT_GROUP_VERBOSE_NAME, None) in pk_set:
            if action == "post_add":
                Student.objects.create(user=instance)
            if action == "pre_remove":
                Student.objects.filter(user=instance.pk).delete()

        if group_mapping.get(settings.TRAINER_GROUP_VERBOSE_NAME, None) in pk_set:
            if action == "post_add":
                Trainer.objects.create(user=instance)
            elif action == "pre_remove":
                Trainer.objects.filter(user=instance.pk).delete()
