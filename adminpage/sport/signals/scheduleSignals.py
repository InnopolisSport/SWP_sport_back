from datetime import date, timedelta, datetime
from typing import Iterator

from django.db.models.signals import post_save, pre_delete
from django.dispatch.dispatcher import receiver
from django.utils import timezone

from sport.models import Schedule, Training


def get_today() -> date:
    return timezone.now().date()


def get_current_monday() -> date:
    today = get_today()
    return today - timedelta(days=today.weekday())


def week_generator(start: date, end: date) -> Iterator[date]:
    """
    Generate monday's date for all weeks between start and date including first and last week

    :param start: start generating on week start belongs to
    :param end: stop generating on week end belongs to
    """
    start -= timedelta(days=start.weekday())
    end -= timedelta(days=end.weekday())
    while start <= end:
        yield start
        start += timedelta(weeks=1)


@receiver(pre_delete, sender=Schedule)
def remove_future_trainings_from_schedule(instance: Schedule, **kwargs):
    """
    Remove future trainings related to the schedule
    """
    # semester = instance.group.semester  # type: Semester
    # since date < datetime comparison cuts datetime, append time till 23:59:59
    # semester_end_datetime = datetime.combine(date=semester.end,
    #                                          time=timezone.make_aware(time(23, 59, 59))
    #                                          )
    Training.objects.filter(group=instance.group,  # trainings belong to group
                            start__gt=timezone.now(),  # end__lte=semester_end_datetime,  # are within semester
                            schedule=instance,  # and
                            ).delete()


@receiver(post_save, sender=Schedule)
def create_trainings_current_semester(instance: Schedule, created, **kwargs):
    # if schedule was changed - then time or date changed,
    # so we recreate all future trainings
    if not created:
        remove_future_trainings_from_schedule(instance, **kwargs)

    semester = instance.group.semester
    today = get_today()
    server_timezone = timezone.get_default_timezone()
    server_time = timezone.make_naive(datetime.now(server_timezone))
    for week_start in week_generator(max(get_current_monday(), semester.start), semester.end):
        training_date = week_start + timedelta(days=instance.weekday)
        if today <= training_date <= semester.end:
            # using naive time here intended, since instance.{start, end}
            # contain aware time (at least by values)
            training_start = datetime.combine(
                date=training_date,
                time=instance.start,
            )
            if server_time < training_start:
                training_end = datetime.combine(
                    date=training_date,
                    time=instance.end,
                )

                Training.objects.create(
                    group=instance.group,
                    schedule=instance,
                    start=training_start,
                    end=training_end,
                    training_class=instance.training_class,
                )
