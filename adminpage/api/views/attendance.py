from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.response import Response

from api.crud import get_email_name_like_students, Training, \
    get_students_grades, mark_hours
from api.permissions import IsTrainer
from api.serializers import SuggestionQuerySerializer, SuggestionSerializer, \
    NotFoundSerializer, InbuiltErrorSerializer, \
    TrainingGradesSerializer, AttendanceMarkSerializer, error_detail, \
    BadGradeReportGradeSerializer, BadGradeReport

User = get_user_model()


class AttendanceErrors:
    TRAINING_NOT_EDITABLE = (
        2,
        f"Training not editable before it or after "
        f"{settings.TRAINING_EDITABLE_INTERVAL.days} days")
    OUTBOUND_GRADES = (
        3, "Some students received negative marks or more than maximum")


def is_training_group(training, trainer):
    if training.group.trainer_id != trainer.pk:
        raise PermissionDenied(
            detail="You are not a trainer of this group"
        )


def compose_bad_grade_report(email: str, hours: float) -> dict:
    return {
        "email": email,
        "hours": hours,
    }


@swagger_auto_schema(
    method="GET",
    query_serializer=SuggestionQuerySerializer,
    responses={
        status.HTTP_200_OK: SuggestionSerializer(many=True),
    }
)
@api_view(["GET"])
@permission_classes([IsTrainer])
def suggest_student(request, **kwargs):
    serializer = SuggestionQuerySerializer(data=request.GET)
    serializer.is_valid(raise_exception=True)
    suggested_students = get_email_name_like_students(
        serializer.validated_data["group_id"],
        serializer.validated_data["term"]
    )
    return Response([
        {
            "value": f"{student['id']}_"
                     f"{student['full_name']}_"
                     f"{student['email']}",
            "label": f"{student['full_name']} "
                     f"({student['email']})",
        }
        for student in suggested_students
    ])


@swagger_auto_schema(
    method="GET",
    responses={
        status.HTTP_200_OK: TrainingGradesSerializer,
        status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        status.HTTP_403_FORBIDDEN: InbuiltErrorSerializer,
    }
)
@api_view(["GET"])
@permission_classes([IsTrainer])
def get_grades(request, training_id, **kwargs):
    trainer = request.user  # trainer.pk == trainer.user.pk
    try:
        training = Training.objects.select_related(
            "group"
        ).only("group__name", "group__trainer", "start").get(pk=training_id)
    except Training.DoesNotExist:
        raise NotFound()

    is_training_group(training, trainer)

    return Response({
        "group_id": training.group_id,
        "group_name": training.group.name,
        "start": training.start,
        "grades": get_students_grades(training_id)
    })


@swagger_auto_schema(
    method="POST",
    request_body=AttendanceMarkSerializer,
    responses={
        status.HTTP_200_OK: BadGradeReportGradeSerializer(many=True),
        status.HTTP_400_BAD_REQUEST: BadGradeReport(),
        status.HTTP_403_FORBIDDEN: InbuiltErrorSerializer,
    }
)
@api_view(["POST"])
@permission_classes([IsTrainer])
def mark_attendance(request, **kwargs):
    serializer = AttendanceMarkSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    trainer = request.user  # trainer.pk == trainer.user.pk
    try:
        training = Training.objects.select_related(
            "group"
        ).only("group__trainer", "start", "end").get(
            pk=serializer.validated_data["training_id"])
    except Training.DoesNotExist:
        raise NotFound()

    is_training_group(training, trainer)

    now = timezone.now()
    if not training.start <= now <= training.start + \
           settings.TRAINING_EDITABLE_INTERVAL:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data=error_detail(*AttendanceErrors.TRAINING_NOT_EDITABLE)
        )

    id_to_hours = dict([
        (item["student_id"], item["hours"])
        for item in serializer.validated_data["students_hours"]
    ])

    max_hours = training.academic_duration
    students = User.objects.filter(pk__in=id_to_hours.keys()).only("email")

    hours_to_mark = []
    negative_mark = []
    overflow_mark = []

    for student in students:
        hours_put = id_to_hours[student.pk]
        if hours_put < 0:
            negative_mark.append(
                compose_bad_grade_report(student.email, hours_put))
        elif hours_put > max_hours:
            overflow_mark.append(
                compose_bad_grade_report(student.email, hours_put))
        else:
            hours_to_mark.append((student, hours_put))

    if negative_mark or overflow_mark:
        return Response(
            status=status.HTTP_400_BAD_REQUEST,
            data={
                **error_detail(*AttendanceErrors.OUTBOUND_GRADES),
                "negative_marks": negative_mark,
                "overflow_marks": overflow_mark,
            }
        )
    else:
        mark_data = [(x[0].pk, x[1]) for x in hours_to_mark]
        mark_hours(training, mark_data)
        return Response(list(
            map(
                lambda x: compose_bad_grade_report(x[0].email, x[1]),
                hours_to_mark
            )
        ))
