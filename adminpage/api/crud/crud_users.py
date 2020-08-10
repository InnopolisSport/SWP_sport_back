from django.db import connection

from api.crud.utils import dictfetchall


def get_email_name_like_students(pattern: str, limit: int = 5):
    """
    Retrieve at most <limit students> which emails start with <email_pattern>
    @param pattern - beginning of student email/name
    @param limit - how many student will be retrieved maximum
    @return list of students that are
    """
    pattern = pattern.lower() + '%'
    with connection.cursor() as cursor:
        cursor.execute('SELECT '
                       'd.id AS id, '
                       'd.first_name AS first_name, '
                       'd.last_name AS last_name, '
                       'd.email AS email,'
                       'd.first_name || \' \' || d.last_name as full_name '
                       'FROM auth_user d '
                       'WHERE d.email LIKE %s or '
                       'lower(d.first_name || \' \' || d.last_name) LIKE %s or '
                       'lower(d.last_name) LIKE %s '
                       'LIMIT %s',
                       (pattern, pattern, pattern, str(limit)))
        return dictfetchall(cursor)
