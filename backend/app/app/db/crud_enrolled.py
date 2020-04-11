import logging
from typing import List, Tuple

from .crud_users import UserTableName, __tuple_to_student
from ..models.user import Student

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def get_enrolled_students(conn, group_id: int) -> List[Student]:
    """
    Retrieves existing sport types
    @param conn - Database connection
    @param group_id - searched group id
    @return list of all enrolled students in a group
    """
    cursor = conn.cursor()
    cursor.execute(f'SELECT s.id, s.first_name, s.last_name, s.email '
                   f'FROM enroll e, {UserTableName.STUDENT.value} s '
                   f'WHERE s.id = e.student_id AND e.group_id = %s', (group_id,))
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
        cursor.execute('INSERT INTO enroll (student_id, group_id) VALUES (%s, %s)', (student_id, group_id))
    conn.commit()


def reenroll_student(conn, group_id: int, student_id: int):
    """
    Enrolls given student in a group, removes all previous enrollments
    @param conn - Database connection
    @param group_id - new enrolled group id
    @param student_id - enrolled student id
    """
    cursor = conn.cursor()
    cursor.execute('DELETE FROM enroll WHERE student_id = %s', (student_id,))
    cursor.execute('INSERT INTO enroll (student_id, group_id) VALUES (%s, %s)', (student_id, group_id))
    conn.commit()


def is_enrolled_anywhere(conn, email: str) -> bool:
    """
    Retrieves existing sport types
    @param conn - Database connection
    @param email - student to check
    @return list of all enrolled students in a group
    """
    cursor = conn.cursor()
    cursor.execute(f'SELECT count(*) '
                   f'FROM enroll e, {UserTableName.STUDENT.value} s '
                   f'WHERE s.email = %s AND e.student_id = s.id', (email,))

    cnt = cursor.fetchone()[0]
    return cnt > 0


def get_enrollment_mapping(conn) -> List[Tuple[str, str]]:
    """
    Generates report for current semester with all enrolled students
    @param conn - Database connection
    @return list of tuples with student email and primary group name
    """
    cursor = conn.cursor()
    cursor.execute(f'SELECT s.email, g.name '
                   f'FROM {UserTableName.STUDENT.value} s '
                   f'LEFT JOIN enroll e ON e.student_id = s.id '
                   f'LEFT JOIN "group" g ON e.group_id = g.id '
                   f'LEFT JOIN semester se ON g.semester_id = se.id '
                   f'AND se.start = (SELECT max(start) FROM semester)')
    return cursor.fetchall()
