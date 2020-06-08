from django.db import connection

from api.crud import dictfetchone


def get_ongoing_semester():
    """
    Retrieves current ongoing semester
    @return ongoing semester
    """
    with connection.cursor() as cursor:
        cursor.execute('SELECT * FROM semester WHERE id = current_semester()')
        return dictfetchone(cursor)
