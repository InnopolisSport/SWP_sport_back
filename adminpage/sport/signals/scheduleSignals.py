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


@receiver(post_save, sender=Schedule)
def create_trainings_current_semester(sender, instance: Schedule, created, **kwargs):
    if created:
        semester = instance.group.semester
        today = get_today()
        for week_start in week_generator(max(get_current_monday(), semester.start), semester.end):
            training_date = week_start + timedelta(days=instance.weekday)
            if today <= training_date <= semester.end:
                training_start = datetime.combine(
                    date=training_date,
                    time=instance.start,
                )
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


django_week_day_map = {
    Schedule.Weekday.SUNDAY: 1,
    Schedule.Weekday.MONDAY: 2,
    Schedule.Weekday.TUESDAY: 3,
    Schedule.Weekday.WEDNESDAY: 4,
    Schedule.Weekday.THURSDAY: 5,
    Schedule.Weekday.FRIDAY: 6,
    Schedule.Weekday.SATURDAY: 7,
}


@receiver(pre_delete, sender=Schedule)
def remove_trainings_from_schedule(sender, instance: Schedule, using, **kwargs):
    """
    Remove future trainings related to the schedule
    """
    # semester = instance.group.semester  # type: Semester
    # since date < datetime comparison cuts datetime, append time till 23:59:59
    # semester_end_datetime = datetime.combine(date=semester.end,
    #                                          time=timezone.make_aware(time(23, 59, 59))
    #                                          )
    Training.objects.filter(group=instance.group,  # trainings belong to group
                            start__gte=timezone.now(),  # end__lte=semester_end_datetime,  # are within semester
                            schedule=instance,  # and
                            ).delete()
