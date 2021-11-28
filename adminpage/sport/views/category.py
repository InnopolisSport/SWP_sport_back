from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from sport.models import Student

from api.crud import get_sports, get_clubs, get_student_groups


def parse_group(group: dict) -> dict:
    return {
        "id": group["id"],
        'qualified_name': f'{group["name"]} ({group["sport_name"]})',
        "name": group["name"],
        "sport": group["sport_name"]
    }


@login_required
def category_view(request, **kwargs):
    student = Student.objects.filter(pk=request.user.pk).select_related(
        "medical_group"
    ).first()
    sports = get_sports(student=student)
    clubs = sorted(
        [{
            "available_places": club["capacity"] - club["current_load"],
            **club,
        }
            for club in get_clubs(student=student)],
        key=lambda group: (group["current_load"] >= group["capacity"], group["name"])
    )
    sc_training_groups = []  # TODO
    student_groups = get_student_groups(student)
    student_groups_parsed = list(map(
        parse_group,
        student_groups
    ))
    return render(request, "category.html", {
        "sports": sports,
        "clubs": clubs,
        "sc_training_groups": sc_training_groups,
        "student": student,
        "student_sport_group": student_groups_parsed,
    })
