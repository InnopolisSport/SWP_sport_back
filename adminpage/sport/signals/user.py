from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ValidationError
from django.db.models.signals import m2m_changed, post_save, pre_save
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
        if group_mapping.get(
                settings.STUDENT_AUTH_GROUP_VERBOSE_NAME,
                None
        ) in pk_set:
            if action == "post_add":
                Student.objects.get_or_create(pk=instance.pk)
            if action == "pre_remove":
                Student.objects.filter(pk=instance.pk).delete()

        if group_mapping.get(
                settings.TRAINER_AUTH_GROUP_VERBOSE_NAME,
                None
        ) in pk_set:
            if action == "post_add":
                Trainer.objects.get_or_create(pk=instance.pk)


@receiver(post_save, sender=Student)
def add_group_for_student_status(instance: Student, sender, using, **kwargs):
    instance.user.groups.remove(*instance.user.groups.filter(name__startswith="STUDENT_STATUS"))
    new_group, created = Group.objects.get_or_create(name="STUDENT_STATUS_{}".format(instance.student_status.id),
                                            defaults={'verbose_name': "[Student status] {}".format(instance.student_status.name)})
    if instance.student_status.name == "Normal":
        new_group.permissions.add(Permission.objects.get(codename='go_to_another_group'))

    instance.user.groups.add(new_group)


@receiver(pre_save, sender=Student)
def validate_student_course(instance: Student, *args, **kwargs):
    if instance.course < 1 or instance.course > 4:
        raise ValidationError("Wrong number of course")


def update_group_verbose_names(sid_to_name_mapping: dict):
    groups = Group.objects.filter(name__in=sid_to_name_mapping.keys())
    for group in groups:
        group.verbose_name = sid_to_name_mapping[group.name]
    Group.objects.bulk_update(groups, ['verbose_name'])


@receiver(post_authenticate)
def verify_bachelor_role(user, claims, adfs_response, *args, **kwargs):
    """
    Remove student account from non-bachelor students
    """
    token_group_mapping = dict(zip(claims["groupsid"], claims["group"]))
    update_group_verbose_names(token_group_mapping)

    if settings.STUDENT_AUTH_GROUP_VERBOSE_NAME in claims["group"] and \
            user.role is not None:
        is_active_student = user.role.startswith(
            settings.BACHELOR_GROUPS_PREFIX
        )
        # To unban mistakenly banned people
        user.is_active = True
        if not is_active_student:
            group_mapping = get_current_group_mapping()
            student_group = group_mapping.get(
                settings.STUDENT_AUTH_GROUP_VERBOSE_NAME,
                None
            )
            user.groups.remove(student_group)
        user.save()
