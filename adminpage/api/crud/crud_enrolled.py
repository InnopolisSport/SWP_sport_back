from sport.models import Student, Enroll, Group
from django.db import transaction


@transaction.atomic
def enroll_student(group: Group, student: Student):
    """
    Enrolls given student in a primary group, removes all previous enrollments
    """
    has_primary = Enroll.objects.filter(student=student, group__semester=group.semester, is_primary=True).exists()
    Enroll.objects.create(student=student, group=group, is_primary=not has_primary)


def unenroll_student(group: Group, student: Student) -> int:
    """
    Unenrolls given student from a secondary group
    """
    removed_count, _ = Enroll.objects.filter(student=student, group=group, is_primary=False).delete()
    return removed_count
