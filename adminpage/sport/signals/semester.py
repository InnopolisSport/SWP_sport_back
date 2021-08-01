import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group as AuthGroup
from django.db.models.signals import post_save, pre_save
from django.dispatch.dispatcher import receiver
from datetime import datetime

from sport.models import Semester, Sport, Trainer, Group, Schedule, Student

from api.crud import get_brief_hours, get_detailed_hours, get_ongoing_semester

User = get_user_model()


def get_or_create_student_group():
    return AuthGroup.objects.get_or_create(
        verbose_name=settings.STUDENT_AUTH_GROUP_VERBOSE_NAME,
        defaults={
            "name": settings.STUDENT_AUTH_GROUP_NAME,
        }
    )[0]


def get_or_create_trainer_group():
    return AuthGroup.objects.get_or_create(
        verbose_name=settings.TRAINER_AUTH_GROUP_VERBOSE_NAME,
        defaults={
            "name": settings.TRAINER_AUTH_GROUP_NAME,
        }
    )[0]


@receiver(post_save, sender=Semester)
def special_groups_create(sender, instance, created, **kwargs):
    if created:
        trainer_group = get_or_create_trainer_group()
        sport_dep_user, _ = User.objects.get_or_create(
            first_name="Sport",
            last_name="Department",
            email=settings.SPORT_DEPARTMENT_EMAIL,
            defaults={
                "is_active": True,
            }
        )
        sport_dep_user.groups.add(trainer_group)
        sport_dep, _ = Trainer.objects.get_or_create(user=sport_dep_user)
        kwargs = {
            'is_club': False,
            'sport': None,
            'semester': instance,
            'trainer': sport_dep
        }
        Group.objects.create(
            name=settings.SELF_TRAINING_GROUP_NAME,
            capacity=9999,
            **kwargs
        )
        Group.objects.create(
            name=settings.EXTRA_EVENTS_GROUP_NAME,
            capacity=0,
            **kwargs,
        )
        Group.objects.create(
            name=settings.MEDICAL_LEAVE_GROUP_NAME,
            capacity=0,
            **kwargs
        )
    else:
        # if semester changed, recalculate all future related schedules
        semester_schedules = Schedule.objects.filter(
            group__semester=instance.pk
        )
        for schedule in semester_schedules:
            post_save.send(
                sender=Schedule,
                instance=schedule,
                created=False
            )


@receiver(pre_save, sender=Semester)
def validate_semester(sender, instance, *args, **kwargs):
    for i in Semester.objects.all():
        if (i.start < instance.start and i.end < instance.start) or \
                (i.start > instance.end and i.end > instance.end):
            pass
        else:
            raise ValueError("Last semester has a intersection with other semester")


@receiver(post_save, sender=Semester)
def start_semester(sender, instance, created, **kwargs):
    students = Student.objects.all()
    for student in students:
        if student.student_status.id != 0:
            pass
        elif student.course == 4:
            student.student_status.id = 3
        else:
            student.course += 1

        if student.medical_group.name in ("Special 1", "Special 2"):
            student.medical_group.id = -2
        student.save()