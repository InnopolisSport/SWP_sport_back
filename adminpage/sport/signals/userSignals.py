from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db.models.signals import m2m_changed
from django.dispatch.dispatcher import receiver
from django_auth_adfs.signals import post_authenticate

from sport.models import Student, Trainer

User = get_user_model()


def get_current_group_mapping():
    group_mapping = {}
    user_groups = Group.objects.filter(
        verbose_name__in=[
            settings.STUDENT_AUTH_GROUP_VERBOSE_NAME,
            settings.TRAINER_AUTH_GROUP_VERBOSE_NAME,
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
        if group_mapping.get(settings.STUDENT_AUTH_GROUP_VERBOSE_NAME,
                             None) in pk_set:
            if action == "post_add":
                Student.objects.get_or_create(pk=instance.pk)
            if action == "pre_remove":
                Student.objects.filter(pk=instance.pk).delete()

        if group_mapping.get(settings.TRAINER_AUTH_GROUP_VERBOSE_NAME,
                             None) in pk_set:
            if action == "post_add":
                Trainer.objects.get_or_create(pk=instance.pk)


@receiver(post_authenticate)
def verify_bachelor_role(user, claims, adfs_response, *args, **kwargs):
    if user.role is not None:
        is_active_student = user.role.startswith("B")
        user.is_active = is_active_student
        if not is_active_student:
            group_mapping = get_current_group_mapping()
            student_group = group_mapping.get(
                settings.STUDENT_AUTH_GROUP_VERBOSE_NAME,
                None
            )
            user.groups.remove(student_group)
        user.save()
