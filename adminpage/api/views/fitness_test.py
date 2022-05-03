from collections import defaultdict

from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from api.permissions import (
    IsTrainer, IsStudent,
)
from api.serializers import (
    FitnessTestResults,
    NotFoundSerializer,
    ErrorSerializer, SuggestionSerializer
)

from api.crud import get_exercises_crud, post_student_exercises_result_crud, \
    get_email_name_like_students, get_ongoing_semester, get_score, get_max_score
from api.serializers.attendance import SuggestionQueryFTSerializer
from api.serializers.fitness_test import FitnessTestSessions, FitnessTestSessionFull, FitnessTestStudentResults
from sport.models import Group, FitnessTestSession, FitnessTestResult, FitnessTestExercise, Semester


def convert_exercise(t: FitnessTestExercise) -> dict:
    return {
        "id": t.id,
        "semester": t.semester.id,
        "name": t.exercise_name,
        "unit": t.value_unit,
        "select": t.select.split(',') if t.select is not None else None,
    }


@api_view(["GET"])
def get_exercises(request, semester_id=None, **kwargs):
    if semester_id is None:
        semester_id = get_ongoing_semester()
    exercises = get_exercises_crud(semester_id)
    result_exercises = [convert_exercise(exercise) for exercise in exercises]
    return Response(result_exercises)

@api_view(["GET"])
def get_all_exercises(request, **kwargs):
    exercises = get_exercises_crud()
    result_exercises = [convert_exercise(exercise) for exercise in exercises]

    return Response(result_exercises)


@swagger_auto_schema(
    method="GET",
    responses={
        status.HTTP_200_OK: FitnessTestSessions
    }
)
@api_view(["GET"])
def get_sessions(request, semester_id=None, **kwargs):
    if semester_id is None:
        sessions = FitnessTestSession.objects.all()
    else:
        sessions = FitnessTestSession.objects.filter(semester_id=semester_id)
    resp = [{'id': s.id, 'semester': s.semester.name, 'date': s.date, 'teacher': str(s.teacher)} for s in sessions]

    return Response(resp)


@swagger_auto_schema(
    method="GET",
    responses={
        status.HTTP_200_OK: FitnessTestStudentResults
    }
)
@api_view(["GET"])
@permission_classes([IsStudent])
def get_result(request, **kwargs):
    results = FitnessTestResult.objects.filter(student_id=request.user.student.user_id)
    if not len(results):
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = []
    for result_distinct_semester in results.values('exercise__semester_id').distinct():
        semester_id = result_distinct_semester['exercise__semester_id']
        semester = Semester.objects.get(id=semester_id)

        total_score = 0
        result_list = []
        for result in results.filter(exercise__semester_id=semester_id):
            result_list.append({
                'exercise': result.exercise.exercise_name,
                'unit': result.exercise.value_unit,
                'value': (result.value
                          if result.exercise.select is None
                          else result.exercise.select.split(',')[result.value]),
                'score': get_score(request.user.student, result),
                'max_score': get_max_score(request.user.student, result),
            })
            grade = result_list[-1]['score'] >= result.exercise.threshold
            total_score += result_list[-1]['score']

        grade = grade and total_score >= semester.points_fitness_test
        data.append({
            'semester': semester.name,
            'grade': grade,
            'total_score': total_score,
            'details': result_list,
        })

    return Response(data=data, status=status.HTTP_200_OK)


@swagger_auto_schema(
    method="GET",
    responses={
        status.HTTP_200_OK: FitnessTestSessionFull,
    }
)
@api_view(["GET"])
def get_session_info(request, session_id, **kwargs):
    session = FitnessTestSession.objects.get(id=session_id)
    session_dict = {'id': session.id, 'semester': session.semester.id, 'date': session.date, 'teacher': str(session.teacher)}

    results = FitnessTestResult.objects.filter(session_id=session.id)

    results_dict = defaultdict(list)
    for result in results:
        results_dict[result.exercise.exercise_name].append(
            {'student_name': f"{result.student.user.first_name} {result.student.user.last_name}",
             'student_email': result.student.user.email,
             'student_id': result.student.user.id,
             'student_medical_group': result.student.medical_group.name,
             'value': result.value})

    response = {'session': session_dict, 'results': results_dict}

    return Response(response)


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
def post_student_exercises_result(request, session_id=None, **kwargs):
    trainer = request.user
    if not trainer.has_perm('sport.change_fitness_test'):
        return Response(
            status=400,
        )
    serializer = FitnessTestResults(data=request.data)
    serializer.is_valid(raise_exception=True)
    exercises = serializer.validated_data['result']
    session = post_student_exercises_result_crud(exercises, session_id, request.user)
    return Response({'session_id': session})


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
        requirement=(~Q(fitnesstestresult__exercise__semester=get_ongoing_semester()))
    )
    return Response([
        {
            "value": f"{student['id']}_"
                     f"{student['full_name']}_"
                     f"{student['email']}_"
                     f"{student['medical_group__name']}_"
                     f"{student['gender']}",
            "label": f"{student['full_name']} "
                     f"({student['email']})",
        }
        for student in suggested_students
    ])
