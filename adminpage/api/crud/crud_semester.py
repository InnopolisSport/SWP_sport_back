from sport.models import Semester


def get_ongoing_semester():
    """
    Retrieves current ongoing semester
    @return ongoing semester
    """
    return Semester.objects.raw('SELECT * FROM semester WHERE id = current_semester()')[0]
