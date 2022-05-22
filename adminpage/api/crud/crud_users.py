from django.db import connection
from django.db.models import F
from django.db.models import Q
from django.db.models import Value
from django.db.models.functions import Concat

from api.crud.utils import dictfetchall
from sport.models import Student, Group


def get_email_name_like_students(pattern: str, limit: int = 5, requirement=~Q(pk=None)):
    """
    Retrieve at most <limit students> which emails start with <email_pattern>
    @param pattern - beginning of student email/name
    @param limit - how many student will be retrieved maximum
    @return list of students that are
    """

    query = Student.objects.annotate(
        id=F('user__id'),
        first_name=F('user__first_name'),
        last_name=F('user__last_name'),
        email=F('user__email'),
        full_name=Concat('user__first_name', Value(' '), 'user__last_name')
    ).filter(
        requirement & (
            Q(email__icontains=pattern) |
            Q(full_name__icontains=pattern) |
            Q(last_name__icontains=pattern)
        )
    ).values(
        'id',
        'first_name',
        'last_name',
        'email',
        'full_name',
        'medical_group__name',
        'gender'
    )[:limit]

    return list(query)


def get_email_name_like_students_filtered_by_group(pattern: str, limit: int = 5, group=None):
    group = Group.objects.get(id=group)

    medical_group_condition = Q(pk=None)
    for medical_group in group.allowed_medical_groups.all():
        medical_group_condition = medical_group_condition | Q(medical_group__id=medical_group.id)

    return get_email_name_like_students(pattern, limit, medical_group_condition)
