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

from api.crud import get_all_exercises, post_student_exercises_result, get_student_pass


def convert_exercises(t) -> dict:
    res = None
    try:
        res = {
        "name": t.exercise.exercise_name,
        "unit": t.exercise.value_unit,
        "score": t.score,
        "start_range": t.start_range,
        "end_range": t.end_range
        }
    except Exception as ex:
        res = {
            "name": t['exercise']['exercise_name'],
            "unit": t['exercise']['value_unit'],
            "score": t['score'],
            "start_range": t['start_range'],
            "end_range": t['end_range']
        }
    return res


@api_view(["GET"])
def get_exercises(request, **kwargs):
    exercises = get_all_exercises()
    return Response(list(map(convert_exercises, exercises)))


@swagger_auto_schema(
    method="POST",
    request_body=FitnessTestResults,
    responses={
        status.HTTP_200_OK: EmptySerializer,
        status.HTTP_404_NOT_FOUND: NotFoundSerializer,
        status.HTTP_400_BAD_REQUEST: ErrorSerializer,
    },
)
@api_view(["POST"])
@permission_classes([IsTrainer])
def post_student_exercises_result(request, **kwargs):
    serializer = FitnessTestResults(data=request.data)
    serializer.is_valid(raise_exception=True)
    score = post_student_exercises_result(serializer.validated_data['student_email'],
                                          serializer.validated_data['result'])
    return Response({"score": score})
