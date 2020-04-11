from datetime import datetime
from typing import Tuple

from ..models.semester import Semester


def __tuple_to_semester(row: Tuple[int, str, datetime, datetime, datetime]) -> Semester:
    id, name, start, end, choice_deadline = row
    return Semester(id=id, name=name, start=start, end=end, choice_deadline=choice_deadline)


def get_ongoing_semester(conn) -> Semester:
    """
    Retrieves current ongoing semester
    @param conn - Database connection
    @return ongoing semester
    """
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, start, "end", choice_deadline FROM semester WHERE id = current_semester()')
    row = cursor.fetchone()
    return __tuple_to_semester(row) if row is not None else None
