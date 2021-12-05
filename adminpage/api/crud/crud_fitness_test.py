from sport.models import FitnessTestResult, FitnessTestExercise, FitnessTestGrading, Student
from api.crud import get_ongoing_semester


def get_all_exercises():
    return list(FitnessTestGrading.objects.filter(semester=get_ongoing_semester()))


# input: array of dicts, where dict: {"exercise_name": <name of exercise>, "value": <score of student result>}
def post_student_exercises_result_crud(student_email: str, exercises: list) -> int:
    student = Student.objects.get(user__email=student_email)
    score = 0
    for i in range(len(exercises)):
        exercise = FitnessTestExercise.objects.get(exercise_name=exercises[i]['exercise_name'])
        grading_score = FitnessTestGrading.objects.get(exercise=exercise, semester=get_ongoing_semester(),
                                                       start_range__lte=exercises[i]["value"],
                                                       end_range__gte=exercises[i]["value"]).score
        score += grading_score
        result = FitnessTestResult.objects.get_or_create(exercise=exercise, semester=get_ongoing_semester(),
                                                         student=student)
        a = exercises[i]['value']
        result.value = a
        result.save()
    return score


def get_student_pass(score: int) -> bool:
    if score <= 50:
        return False
    else:
        return True
