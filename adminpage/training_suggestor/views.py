from typing import List

from django.contrib.auth import get_user_model
from drf_yasg import openapi
from drf_yasg.openapi import Schema
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.serializers import EmptySerializer, NotFoundSerializer
from training_suggestor.algo import suggest_algo
from training_suggestor.enums import ExerciseTypeChoices
from training_suggestor.models import ExerciseParams, User, Poll, PollResult, PollAnswer
from training_suggestor.serializers import TrainingSerializer, ExerciseParamsSerializer, PollSerializer, \
    PollResultSerializer, UserSerializer
from training_suggestor.utils import recalculate_ratios

djUser = get_user_model()

BLOCK_DISTRIBUTION = {
    'WU': (0.2, 2),
    'PS': (0.15, 2),
    'MS': (0.575, 5),
    'CD': (0.075, 1),
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
        # openapi.Parameter(
        #     name="user",
        #     in_=openapi.IN_QUERY,
        #     type=openapi.TYPE_STRING,
        #     description="Telegram user id",
        #     required=True,
        # ),
    ],
    responses={
        status.HTTP_200_OK: TrainingSerializer(),
    }
)
@api_view(["GET"])
def suggest(request, **kwargs):
    request_working_load = int(request.query_params.get("working_load"))
    request_time = int(request.query_params.get("time"))
    # request_user = request.query_params.get("user")
    # user = User.objects.get_or_create(name=request_user)
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


@swagger_auto_schema(
    method="GET",
    responses={
        status.HTTP_200_OK: PollSerializer(),
        status.HTTP_404_NOT_FOUND: NotFoundSerializer(),
    }
)
@api_view(["GET"])
def get_poll(request, name: str, **kwargs):
    poll = get_object_or_404(Poll, name=name)
    return Response(PollSerializer(poll).data)


@swagger_auto_schema(
    method="POST",
    request_body=PollResultSerializer(),
    responses={
        status.HTTP_200_OK: EmptySerializer(),
    }
)
@api_view(["POST"])
def add_poll_result(request, **kwargs):
    serializer = PollResultSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        result = serializer.save()
        recalculate_ratios(result)
        return Response({})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="GET",
    responses={
        status.HTTP_200_OK: PollResultSerializer(),
        status.HTTP_404_NOT_FOUND: NotFoundSerializer(),
    }
)
@api_view(["GET"])
def get_poll_result(request, poll_name: str, **kwargs):
    poll = get_object_or_404(PollResult, poll__name=poll_name, user=request.user.student.training_suggestor_user)
    return Response(PollResultSerializer(poll).data)


@swagger_auto_schema(
    method="GET",
    responses={
        status.HTTP_200_OK: UserSerializer(many=True),
        status.HTTP_404_NOT_FOUND: NotFoundSerializer(),
    }
)
@api_view(["GET"])
@permission_classes([IsStaff])
def get_telegram_users(request, **kwargs):
    users = djUser.objects.filter(telegram_id__isnull=False)
    return Response(UserSerializer(users, many=True).data)
