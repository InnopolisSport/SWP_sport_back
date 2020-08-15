import pytest
from datetime import datetime, date

from api.crud import get_ongoing_semester
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
    assert qs.count() == 5


@pytest.mark.django_db
def test_get_ongoing_semester(semester_factory):
    semester_factory(name="S19", start=date(2020, 1, 1), end=date(2020, 1, 3), choice_deadline=date(2020, 1, 2))
    s2 = semester_factory(name="S20", start=date(2020, 1, 4), end=date(2020, 1, 24), choice_deadline=date(2020, 1, 20))

    assert get_ongoing_semester() == s2
