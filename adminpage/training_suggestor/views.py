from typing import List

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from training_suggestor.algo import suggest_algo
from training_suggestor.enums import ExerciseTypeChoices
from training_suggestor.models import ExerciseParams
from training_suggestor.serializers import TrainingSerializer, ExerciseParamsSerializer

BLOCK_DISTRIBUTION = {
    'WU': (0.2, 2),
    'PS': (0.15, 2),
    'MS': (0.575, 5),
    'CD': (0.075, 2),
}


@swagger_auto_schema(
    method="GET",
    manual_parameters=[
        openapi.Parameter(
            name="working_load",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description="Working load",
            required=True,
        ),
        openapi.Parameter(
            name="time",
            in_=openapi.IN_QUERY,
            type=openapi.TYPE_INTEGER,
            description="Time",
            required=True,
        ),
    ],
    responses={
        status.HTTP_200_OK: TrainingSerializer(),
    }
)
@api_view(["GET"])
def suggest(request, **kwargs):
    request_working_load = int(request.query_params.get("working_load"))
    request_time = int(request.query_params.get("time"))
    a: List[ExerciseParams] = []
    for key, value in BLOCK_DISTRIBUTION.items():
        exercises = ExerciseParams.objects.filter(type=key)
        working_load = value[0] * request_working_load
        time = value[0] * request_time
        print(working_load, time, value[1])
        suggested = suggest_algo(exercises, working_load=working_load, time=time, number_of_exercises=value[1])
        print(suggested)
        a += suggested
    print(sum([e.working_load for e in a]), sum([e.full_time.total_seconds() for e in a]))
    return Response(TrainingSerializer({'exercises': a}).data)
