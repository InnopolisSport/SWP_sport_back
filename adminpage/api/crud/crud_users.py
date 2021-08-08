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
    # pattern = pattern.lower() + '%'
    # with connection.cursor() as cursor:
    #     cursor.execute('SELECT '
    #                    'd.id AS id, '
    #                    'd.first_name AS first_name, '
    #                    'd.last_name AS last_name, '
    #                    'd.email AS email,'
    #                    'd.first_name || \' \' || d.last_name as full_name '
    #                    'FROM auth_user d, student s '
    #                    'WHERE s.user_id = d.id '
    #                    'AND NULLIF('
    #                    '    (SELECT sign(minimum_medical_group_id) FROM "group" WHERE id = %(group_id)s),'
    #                    '    sign(s.medical_group_id)'
    #                    ') is NULL ' # only true when first arg is NULL, or args are equal
    #                    'AND (d.email LIKE %(pattern)s OR '
    #                    'LOWER(d.first_name || \' \' || d.last_name) LIKE %(pattern)s OR '
    #                    'LOWER(d.last_name) LIKE %(pattern)s) '
    #                    'LIMIT %(limit)s',
    #                    {
    #                        "pattern": pattern,
    #                        "limit": str(limit),
    #                        "group_id": group_id
    #                    })
    #     return dictfetchall(cursor)
    group = Group.objects.get(id=group_id)

    medical_group_condition = Q()
    for medical_group in group.allowed_medical_groups.all():
        medical_group_condition = medical_group_condition | Q(medical_group__id=medical_group.id)

    query = Student.objects.select_related(
        'user',
    ).values(
        'user__id',
        'user__first_name',
        'user__last_name',
        'user__email',
    ).annotate(
        id=F('user__id'),
        first_name=F('user__first_name'),
        last_name=F('user__last_name'),
        email=F('user__email'),
        full_name=Concat('user__first_name', Value(' '), 'user__last_name')
    ).filter(
        medical_group_condition & (
            Q(email__icontains=pattern) |
            Q(full_name__icontains=pattern) |
            Q(last_name__icontains=pattern)
        )
    )[:limit]

    return query