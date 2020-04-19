import logging
from datetime import datetime
from math import floor
from typing import List, Tuple, Optional, Iterable

from .crud_users import __tuple_to_student
from ..models.attendance import AttendanceSemester, AttendanceTraining
from ..models.user import Student

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
    cursor.execute('SELECT s.id, s.name, sum(a.hours) '
                   'FROM semester s, training t, "group" g, attendance a '
                   'WHERE a.student_id = %s '
                   'AND a.training_id = t.id '
                   'AND t.group_id = g.id '
                   'GROUP BY s.id', (student_id,))
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
        cursor.execute('SELECT g.name, t.start, a.hours '
                       'FROM semester s, training t, "group" g, attendance a '
                       'WHERE a.student_id = %s '
                       'AND a.training_id = t.id '
                       'AND t.group_id = g.id '
                       'AND g.semester_id = s.id '
                       'AND s.start = (SELECT max(start) FROM semester)', (student_id,))
    else:
        cursor.execute('SELECT g.name, t.start, a.hours '
                       'FROM training t, "group" g, attendance a '
                       'WHERE a.student_id = %s '
                       'AND a.training_id = t.id '
                       'AND t.group_id = g.id '
                       'AND g.semester_id = %s', (student_id, semester_id))
    rows = cursor.fetchall()
    return list(map(__tuple_to_training_attendance, rows))


def mark_hours(conn, training_id: id, student_hours: Iterable[Tuple[int, float]]):
    """
    Puts hours for one training session to one student. If hours for session were already put, updates it

    @param conn - Database connection
    @param training_id - searched training id
    @param student_hours: iterable with items (<student_id:int>, <student_hours:float>)
    """
    for student_id, student_mark in student_hours:
        if student_id <= 0 or student_mark <= 0.0:
            raise ValueError(f"All students id and marks must be positive, got {(student_id, student_mark)}")
        # Currently hours field is numeric(3,2), so
        # A field with precision 3, scale 2 must round to an absolute value less than 10^1.
        floor_max = 10
        if floor(student_mark) >= floor_max:
            raise ValueError(f"All students marks must floor to less than {floor_max}, "
                             f"got {student_mark} -> {floor(student_mark)} >= {floor_max}")
    cursor = conn.cursor()
    args_str = b",".join(
        cursor.mogrify("(%s, %s, %s)", (student_id, training_id, student_mark))
        for student_id, student_mark in student_hours
    )
    cursor.execute(f'INSERT INTO attendance (student_id, training_id, hours) VALUES {args_str.decode()} '
                   f'ON CONFLICT ON CONSTRAINT unique_attendance '
                   f'DO UPDATE set hours=excluded.hours')
    conn.commit()


def get_training_participants(conn, training_id: int) -> List[Student]:
    """
    Retrieves all students, who should come to the training
    @param conn - Database connection
    @param training_id - Searched training id
    @return list of students
    """
    cursor = conn.cursor()
    cursor.execute('SELECT s.id, s.first_name, s.last_name, s.email '
                   'FROM training t, "group" g, enroll e, student s '
                   'WHERE t.id = %s '
                   'AND s.is_ill = FALSE '
                   'AND g.id = t.group_id '
                   'AND e.student_id = s.id '
                   'AND e.group_id = g.id', (training_id,))
    rows = cursor.fetchall()
    return list(map(__tuple_to_student, rows))


def toggle_illness(conn, student_id: int):
    """
    Toggles student's illness
    @param conn - Database connection
    @param student_id - Searched student id
    """
    cursor = conn.cursor()
    cursor.execute('UPDATE student SET is_ill = not is_ill WHERE id = %s', (student_id,))
    conn.commit()
