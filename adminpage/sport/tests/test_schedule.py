from datetime import datetime, time, date

import pytest

from sport.models import Group, Schedule, Training


@pytest.mark.django_db
@pytest.mark.freeze_time('2020-01-20 10:03')
def test_training_creation_on_schedule(
        semester_factory,
        sport_factory,
        group_factory,
        schedule_factory,
):
    start = date(2020, 1, 20)
    end = date(2020, 1, 27)
    choice_deadline = datetime(2020, 2, 1)
    sem = semester_factory(
        name="S20",
        start=start,
        end=end,
        choice_deadline=choice_deadline,
    )

    sport = sport_factory(
        name="football",
        special=False,
    )

    group = group_factory(
        name="F-S20-01",
        capacity=30,
        sport=sport,
        semester=sem,

    )

    schedule_start = time(14, 0, 0)
    schedule_end = time(18, 30, 0)
    schedule = schedule_factory(
        group=group,
        weekday=Schedule.Weekday.MONDAY,
        start=schedule_start,
        end=schedule_end,
    )

    assert Training.objects.filter(schedule=schedule).count() == 2
