from django.shortcuts import get_object_or_404
from django.utils import timezone
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from api.permissions import (
    IsTrainer,
)
from api.serializers import (
    FitnessTestResults,
    EmptySerializer,
    NotFoundSerializer,
    ErrorSerializer
)

from api.crud import get_all_exercises, post_student_exercises_result_crud, get_student_pass


def convert_exercise(t) -> dict:
    return {
        "name": t.exercise.exercise_name,
        "unit": t.exercise.value_unit,
        "select": t.exercise.select.split(',') if t.exercise.select is not None else None,
        "score": [t.score],
        "start_range": [t.start_range],
        "end_range": [t.end_range]
    }


@api_view(["GET"])
def get_exercises(request, **kwargs):
    exercises = get_all_exercises()
    return Response(list(map(convert_exercise, exercises)))


@swagger_auto_schema(
    method="POST",
    request_body=FitnessTestResults,
    responses={
        status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        status.HTTP_400_BAD_REQUEST: ErrorSerializer,
    },
)
@api_view(["POST"])
@permission_classes([IsTrainer])
def post_student_exercises_result(request, **kwargs):
    serializer = FitnessTestResults(data=request.data)
    serializer.is_valid(raise_exception=True)
    exercises = serializer.validated_data['result']
    post_student_exercises_result_crud(exercises)
    return Response({})
