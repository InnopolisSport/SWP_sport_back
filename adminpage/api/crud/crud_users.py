from django.db import connection
from django.db.models import F
from django.db.models import Q
from django.db.models import Value
from django.db.models.functions import Concat

from api.crud.utils import dictfetchall
from sport.models import Student, Group


def get_email_name_like_students(group_id: int, pattern: str, limit: int = 5):
    """
    Retrieve at most <limit students> which emails start with <email_pattern>
    @param pattern - beginning of student email/name
    @param limit - how many student will be retrieved maximum
    @return list of students that are
    """
    group = Group.objects.get(id=group_id)
    medical_group_condition = Q(pk=None)
    for medical_group in group.allowed_medical_groups.all():
        medical_group_condition = medical_group_condition | Q(medical_group__id=medical_group.id)

    query = Student.objects.annotate(
        id=F('user__id'),
        first_name=F('user__first_name'),
        last_name=F('user__last_name'),
        email=F('user__email'),
        full_name=Concat('user__first_name', Value(' '), 'user__last_name')
    ).filter(
        medical_group_condition & Q(sport=group.sport) & (
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
    )[:limit]

    return list(query)