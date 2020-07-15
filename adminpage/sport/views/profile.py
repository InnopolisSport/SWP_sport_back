from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone

from api.crud import get_ongoing_semester, get_student_groups, get_brief_hours, get_trainer_groups
from sport.models import Student


def parse_group(group: dict) -> dict:
    return {
        "id": group["id"],
        "is_primary": group.get("is_primary", None),
        'qualified_name': f'{group["name"]} ({group["sport_name"]})',
        "name": group["name"],
        "sport": group["sport_name"]
    }


@login_required
def profile_view(request, **kwargs):
    user = request.user

    student = Student.objects.filter(pk=user.pk).select_related("medical_group").first()  # type: Optional[Student]
    trainer = getattr(user, "trainer", None)  # type: Optional[Trainer]

    current_semester = get_ongoing_semester()
    utc_date = timezone.localdate(timezone=timezone.utc)

    context = {
        "user": request.user,
        "common": {
            "semester_name": current_semester.name,
            "enroll_open": current_semester.start <= utc_date <= current_semester.choice_deadline
        },
    }

    if student is not None:
        student_groups = get_student_groups(student)
        student_groups_parsed = list(map(
            parse_group,
            student_groups
        ))
        student_brief_hours_info = get_brief_hours(student)
        student_data = student.__dict__

        context.update({
            "student": {
                "student_id": student.pk,
                "sport_groups": student_groups_parsed,
                "secondary_group_left": 3 - len(student_groups_parsed),
                "semesters": student_brief_hours_info,
                "obj": student,
                **student_data,
            },
        })

    if trainer is not None:
        training_groups = list(map(
            parse_group,
            get_trainer_groups(trainer)
        ))
        trainer_data = trainer.__dict__
        context.update({
            "trainer": {
                "sport_groups": training_groups,
                "obj": trainer,
                **trainer_data,
            },
        })

    return render(request, "profile.html", context)
