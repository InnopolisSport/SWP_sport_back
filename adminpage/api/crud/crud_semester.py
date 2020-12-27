from sport.models import Semester


def get_ongoing_semester() -> Semester:
    """
    Retrieves current ongoing semester
    @return ongoing semester
    """
    return Semester.objects.raw('SELECT * FROM semester WHERE id = current_semester()')[0]
