from sport.models import FitnessTestResult, FitnessTestExercise, FitnessTestGrading, Student
from api.crud import get_ongoing_semester


def get_all_exercises():
    return FitnessTestGrading.objects.filter(semester=get_ongoing_semester())


# input: array of dicts, where dict: {"name": <name of exercise>, "value": <score of student result>}
def post_student_exercises_result(student_email, exercises):
    student = Student.objects.get(email=student_email)
    score = 0
    for i in range(len(exercises)):
        exercise = FitnessTestExercise.objects.filter(exercise_name=exercises[i]['name'])
        grading_score = FitnessTestGrading.objects.filter(exercise=exercise, semester=get_ongoing_semester(),
                                                          start_range__lqt=exercises[i]['score'],
                                                          end_range__gqt=exercises[i]['score']).score
        score += grading_score
        result = FitnessTestResult.objects.get_or_create(exercise=exercise, semester=get_ongoing_semester(),
                                                         student=student)
        result.value = exercises[i]['value']
        result.save()
    return score


def get_student_pass(score: int):
    if score <= 50:
        return False
    else:
        return True
