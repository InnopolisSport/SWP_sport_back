from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone

from api.crud import get_trainings_in_time, get_trainings_for_student, get_trainings_for_trainer
from api.permissions import IsStudent, IsTrainer
from api.serializers import CalendarRequestSerializer, CalendarSerializer


def convert_training(t) -> dict:
    return {
        "title": t["group_name"],
        "start": timezone.localtime(
            t["start"],
        ),
        "end": timezone.localtime(
            t["end"],
        ),
        "extendedProps": {
            "id": t["id"],
            "group_id": t["group_id"],
            "training_class": t["training_class"],
            "current_load": t["current_load"],
            "capacity": t["capacity"],
        }
    }


def convert_personal_training(t) -> dict:
    start_time = timezone.localtime(
        t["start"],
    )
    return {
        "title": t["group_name"],
        "start": start_time,
        "end": timezone.localtime(
            t["end"],
        ),
        "extendedProps": {
            "id": t["id"],
            "can_edit":
                start_time <= timezone.localtime() <= start_time + settings.TRAINING_EDITABLE_INTERVAL,
            "group_id": t["group_id"],
            "can_grade": t["can_grade"],
            "training_class": t["training_class"],
        }
    }


@swagger_auto_schema(
    method="GET",
    query_serializer=CalendarRequestSerializer,
    responses={
        status.HTTP_200_OK: CalendarSerializer,
    }
)
@api_view(["GET"])
def get_schedule(request, sport_id, **kwargs):
    serializer = CalendarRequestSerializer(data=request.GET)
    serializer.is_valid(raise_exception=True)
    trainings = get_trainings_in_time(
        sport_id,
        serializer.validated_data["start"],
        serializer.validated_data["end"],
    )

    return Response(list(map(convert_training, trainings)))


@swagger_auto_schema(
    method="GET",
    query_serializer=CalendarRequestSerializer,
    responses={
        status.HTTP_200_OK: CalendarSerializer,
    }
)
@api_view(["GET"])
@permission_classes([IsStudent | IsTrainer])
def get_personal_schedule(request, **kwargs):
    serializer = CalendarRequestSerializer(data=request.GET)
    serializer.is_valid(raise_exception=True)

    student_trainings = []
    trainer_trainings = []

    if hasattr(request.user, "student"):
        student_trainings = get_trainings_for_student(
            request.user.student,
            serializer.validated_data["start"],
            serializer.validated_data["end"],
        )

    if hasattr(request.user, "trainer"):
        trainer_trainings = get_trainings_for_trainer(
            request.user.trainer,
            serializer.validated_data["start"],
            serializer.validated_data["end"],
        )

    result_dict = dict([
        (training["id"], training)
        for training in student_trainings + trainer_trainings
    ])

    return Response(
        list(map(convert_personal_training, result_dict.values()))
    )
