import logging
from datetime import datetime
from typing import List, Tuple, Optional

from ..models.attendance import AttendanceSemester, AttendanceTraining

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def __tuple_to_attendance(row: Tuple[int, str, float]) -> AttendanceSemester:
    semester_id, semester_name, hours = row
    return AttendanceSemester(semester_id=semester_id, semester_name=semester_name, hours=hours)


def __tuple_to_training_attendance(row: Tuple[str, datetime, float]) -> AttendanceTraining:
    group, timestamp, hours = row
    return AttendanceTraining(group=group, timestamp=timestamp, hours=hours)


def get_brief_hours(conn, student_id: int) -> List[AttendanceSemester]:
    """
    Retrieves statistics of hours per different semesters
    @param conn - Database connection
    @param student_id - searched student id
    @return list of tuples (semester, hours)
    """
    cursor = conn.cursor()
    cursor.execute(f'SELECT s.id, s.name, sum(a.hours) '
                   f'FROM semester s, training t, "group" g, attendance a '
                   f'WHERE a.student_id = %s '
                   f'AND a.training_id = t.id '
                   f'AND t.group_id = g.id '
                   f'GROUP BY s.id', (student_id,))
    rows = cursor.fetchall()
    return list(map(__tuple_to_attendance, rows))


def get_detailed_hours(conn, student_id: int, semester_id: Optional[int] = None) -> List[AttendanceTraining]:
    """
    Retrieves statistics of hours in one semester, by default last one
    @param conn - Database connection
    @param student_id - searched student id
    @param semester_id - searched semester id
    @return list of tuples (semester, hours)
    """
    cursor = conn.cursor()
    if semester_id is None:
        cursor.execute(f'SELECT g.name, t.start, a.hours '
                       f'FROM semester s, training t, "group" g, attendance a '
                       f'WHERE a.student_id = %s '
                       f'AND a.training_id = t.id '
                       f'AND t.group_id = g.id '
                       f'AND g.semester_id = s.id '
                       f'AND s.start = (SELECT max(start) FROM semester)', (student_id,))
    else:
        cursor.execute(f'SELECT g.name, t.start, a.hours '
                       f'FROM training t, "group" g, attendance a '
                       f'WHERE a.student_id = %s '
                       f'AND a.training_id = t.id '
                       f'AND t.group_id = g.id '
                       f'AND g.semester_id = %s', (student_id, semester_id))
    rows = cursor.fetchall()
    return list(map(__tuple_to_training_attendance, rows))


def mark_hours(conn, student_id: int, training_id: id, hours: float):
    """
    Puts hours for one training session to one student
    @param conn - Database connection
    @param student_id - searched student id
    @param training_id - searched training id
    @param hours - marked hours
    """
    cursor = conn.cursor()
    cursor.execute('INSERT INTO attendance (student_id, training_id, hours) VALUES (%s, %s, %s)',
                   (student_id, training_id, hours))
    conn.commit()
