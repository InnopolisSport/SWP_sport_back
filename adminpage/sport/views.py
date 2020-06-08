from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from api.crud import get_ongoing_semester, get_student_groups, get_trainer_groups, get_brief_hours, get_sports, \
    get_clubs, get_sc_training_group
from sport.models import Student


def parse_group(group: dict) -> dict:
    return {
        "id": group["id"],
        "is_primary": group.get("is_primary", None),
        'qualified_name': f'{group["name"]} ({group["sport_name"]})',
        "name": group["name"],
        "sport": group["sport_name"]
    }


def profile_view(request, **kwargs):
    user = request.user

    student = getattr(user, "student", None)  # type: Student
    trainer = getattr(user, "trainer", None)

    current_semester = get_ongoing_semester()
    utc_date = timezone.localdate(timezone=timezone.utc)

    student_groups = get_student_groups(student)
    student_groups_parsed = list(map(
        parse_group,
        student_groups
    ))
    student_brief_hours_info = get_brief_hours(student)
    student_data = student.__dict__

    training_groups = list(map(
        parse_group,
        get_trainer_groups(trainer)
    ))
    trainer_data = student.__dict__

    return render(request, "profile.html", {
        "user": request.user,
        "common": {
            "semester_name": current_semester["name"],
            "enroll_open": current_semester["start"] <= utc_date <= current_semester["choice_deadline"]
        },
        "student": {
            "student_id": student.pk,
            "sport_groups": student_groups_parsed,
            "secondary_group_left": 3 - len(student_groups_parsed),
            "semesters": student_brief_hours_info,
            **student_data,
        },
        "trainer": {
            "sport_groups": training_groups,
            **trainer_data,
        },
    })


def category_view(request, **kwargs):
    sports = get_sports()
    clubs = sorted(
        [{
            "available_places": club["capacity"] - club["current_load"],
            **club,
        }
            for club in get_clubs()],
        key=lambda group: (group["current_load"] >= group["capacity"], group["name"])
    )
    sc_training_group_id = get_sc_training_group()["id"]
    return render(request, "category.html", {
        "sports": sports,
        "clubs": clubs,
        "sc_training_group_id": sc_training_group_id,
    })


def calendar_view(request, sport_id, **kwargs):
    return HttpResponse("Not implemented")
