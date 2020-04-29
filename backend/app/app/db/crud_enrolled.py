import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def enroll_student_to_primary_group(conn, group_id: int, student_id: int) -> None:
    """
    Enrolls given student in a primary group, removes all previous primary enrollments
    @param conn - Database connection
    @param group_id - new enrolled group id
    @param student_id - enrolled student id
    """
    cursor = conn.cursor()
    cursor.execute(
        'DELETE FROM enroll '
        'WHERE student_id = %s '
        'AND is_primary = TRUE '
        'AND group_id IN '
        '(SELECT id FROM "group" WHERE semester_id = (SELECT semester_id FROM "group" WHERE id = %s))',
        (student_id, group_id))
    cursor.execute('INSERT INTO enroll (student_id, group_id, is_primary) VALUES (%s, %s, TRUE)',
                   (student_id, group_id))
    conn.commit()


def enroll_student_to_secondary_group(conn, group_id: int, student_id: int) -> None:
    """
    Enrolls given student to a secondary group
    @param conn - Database connection
    @param group_id - new enrolled group id
    @param student_id - enrolled student id
    """
    cursor = conn.cursor()
    cursor.execute('INSERT INTO enroll (student_id, group_id, is_primary) VALUES (%s, %s, FALSE)',
                   (student_id, group_id))
    conn.commit()


def unenroll_student(conn, group_id: int, student_id: int) -> None:
    """
    Unenrolls given student from a secondary group
    @param conn - Database connection
    @param group_id - new enrolled group id
    @param student_id - enrolled student id
    """
    cursor = conn.cursor()
    cursor.execute('DELETE FROM enroll WHERE group_id = %s AND student_id = %s AND is_primary = FALSE',
                   (group_id, student_id))
    conn.commit()
