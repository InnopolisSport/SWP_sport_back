from sport.models import FitnessTestResult, FitnessTestExercise, FitnessTestGrading, Student
from api.crud import get_ongoing_semester


def get_all_exercises():
    return list(FitnessTestGrading.objects.filter(semester=get_ongoing_semester()))


def post_student_exercises_result_crud(results):
    for res in results:
        student = Student.objects.get(user__id=res['student_id'])
        exercise = FitnessTestExercise.objects.get(exercise_name=res['exercise_name'])
        FitnessTestResult.objects.get_or_create(exercise=exercise, semester=get_ongoing_semester(),
                                                student=student, defaults={'value': res['value']})


def get_student_score(student: Student):
    score = 0
    results = FitnessTestResult.objects.filter(student=student, semester=get_ongoing_semester())
    for result in results:
        score += FitnessTestGrading.objects.get(exercise=result.exercise, semester=get_ongoing_semester(),
                                                start_range__lte=result.value, end_range__gte=result.value).score
