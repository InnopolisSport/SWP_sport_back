from sport.models import Student, Enroll, Group
from django.db import transaction


@transaction.atomic
def enroll_student(group: Group, student: Student):
    """
    Enrolls given student in a group
    """
    Enroll.objects.create(student=student, group=group)


def unenroll_student(group: Group, student: Student) -> int:
    """
    Unenroll given student from a group, leaving at least 1 enroll
    """
    enrollment_count = Enroll.objects.filter(
        student=student,
        group__semester=group.semester
    ).count()
    removed_count = 0
    if enrollment_count > 1:
        removed_count, _ = Enroll.objects.filter(
            student=student,
            group=group,
        ).delete()
    return removed_count
