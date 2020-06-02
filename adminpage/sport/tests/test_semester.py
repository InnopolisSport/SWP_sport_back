from datetime import datetime

import pytest

from sport.models import Group


@pytest.mark.django_db
def test_special_groups_creation(
        semester_factory,
):
    start = datetime(2020, 1, 20)
    end = datetime(2020, 5, 20)
    choice_deadline = datetime(2020, 2, 1)
    semester_factory(
        name="S20",
        start=start,
        end=end,
        choice_deadline=choice_deadline,
    )
    qs = Group.objects.filter(sport__special=True)
    assert qs.count() == 2
