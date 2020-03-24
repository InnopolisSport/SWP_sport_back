from typing import List
from .crud_users import UserTableName, __tuple_to_student
from ..models.user import Student


def get_enrolled_students(conn, group_id: int) -> List[Student]:
    """
    Retrieves existing sport types
    @param conn - Database connection
    @param group_id - searched group id
    @return list of all enrolled students in a group
    """
    cursor = conn.cursor()
    cursor.execute('SELECT s.id, s.first_name, s.last_name, s.email'
                   'FROM enrolled e, %s s '
                   'WHERE s.id = e.student_id AND e.group_id = %s', (UserTableName, group_id))
    rows = cursor.fetchall()
    return list(map(__tuple_to_student, rows))


def enroll_students(conn, group_id: int, students: List[int]):
    """
    Enrolls all given students in a group
    @param conn - Database connection
    @param group_id - searched group id
    @param students - list of enrolled student ids
    """
    cursor = conn.cursor()
    for student_id in students:
        cursor.execute('INSERT INTO enrolled (student_id, group_id) VALUES (%s, %s)', (student_id, group_id))
    conn.commit()
