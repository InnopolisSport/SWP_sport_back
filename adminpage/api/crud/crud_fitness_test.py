import datetime

from django.db.models import QuerySet, Q

from sport.models import FitnessTestResult, FitnessTestExercise, FitnessTestGrading, Student, FitnessTestSession
from api.crud import get_ongoing_semester


def get_all_exercises():
    return list(FitnessTestGrading.objects.filter(semester=get_ongoing_semester()))


def post_student_exercises_result_crud(results, session_id, teacher):
    session, created = FitnessTestSession.objects.get_or_create(id=session_id, defaults={'teacher_id': teacher.id, 'date': datetime.datetime.now()})
    # print(session)
    for res in results:
        student = Student.objects.get(user__id=res['student_id'])
        exercise = FitnessTestExercise.objects.get(
            exercise_name=res['exercise_name'])
        FitnessTestResult.objects.update_or_create(exercise=exercise, semester=get_ongoing_semester(),
                                                   student=student, defaults={'value': res['value']}, session=session)
    return session.id


def get_grading_scheme(student: Student, result: FitnessTestResult):
    return FitnessTestGrading.objects.filter(Q(gender__exact=-1) | Q(gender__exact=student.gender),
                                             exercise=result.exercise,
                                             semester=get_ongoing_semester())


def get_score(student: Student, result: FitnessTestResult):
    return get_grading_scheme(student, result).get(start_range__lte=result.value, end_range__gt=result.value).score


def get_max_score(student: Student, result: FitnessTestResult):
    return max(map(lambda x: x[0], get_grading_scheme(student, result).values_list('score')))
