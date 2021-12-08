from django.db.models import Q
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
    ErrorSerializer, SuggestionQuerySerializer, SuggestionSerializer
)

from api.crud import get_all_exercises, post_student_exercises_result_crud, \
    get_email_name_like_students
from api.serializers.attendance import SuggestionQueryFTSerializer
from sport.models import Group


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
    result_exercises = []
    
    for exercise in exercises:
        exercise_dict = convert_exercise(exercise)
        x = list(map(lambda x: x if x['name'] == exercise_dict['name'] else None, result_exercises))
        x = [element for element in x if element != None]
        if len(x) != 0:
            print(x)
            print(result_exercises)
            exercise_index = result_exercises.index(x[0])
            result_exercises[exercise_index]['score'].append(exercise_dict['score'][0])
            result_exercises[exercise_index]['start_range'].append(exercise_dict['start_range'][0])
            result_exercises[exercise_index]['end_range'].append(exercise_dict['end_range'][0])
        else:
            result_exercises.append(exercise_dict)
    return Response(result_exercises)


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
    trainer = request.user
    if not trainer.has_perm('sport.change_fitness_test'):
        return Response(
            status=400,
        )
    serializer = FitnessTestResults(data=request.data)
    serializer.is_valid(raise_exception=True)
    exercises = serializer.validated_data['result']
    post_student_exercises_result_crud(exercises)
    return Response({})


@swagger_auto_schema(
    method="GET",
    query_serializer=SuggestionQueryFTSerializer,
    responses={
        status.HTTP_200_OK: SuggestionSerializer(many=True),
    }
)
@api_view(["GET"])
@permission_classes([IsTrainer])
def suggest_fitness_test_student(request, **kwargs):
    serializer = SuggestionQueryFTSerializer(data=request.GET)
    serializer.is_valid(raise_exception=True)

    suggested_students = get_email_name_like_students(
        serializer.validated_data["term"],
        requirement=(~Q(fitnesstestresult__semester=15))
    )
    return Response([
        {
            "value": f"{student['id']}_"
                     f"{student['full_name']}_"
                     f"{student['email']}_"
                     f"{student['medical_group__name']}",
            "label": f"{student['full_name']} "
                     f"({student['email']})",
        }
        for student in suggested_students
    ])
