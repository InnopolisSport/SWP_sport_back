from math import floor
from typing import Iterable, Tuple

from django.db import connection

from api.crud.utils import dictfetchall
from sport.models import Student, Semester, Training


def get_brief_hours(student: Student):
    """
    Retrieves statistics of hours per different semesters
    """
    with connection.cursor() as cursor:
        cursor.execute('SELECT '
                       's.id AS semester_id, '
                       's.name AS semester_name, '
                       's.start AS semester_start, '
                       's.end AS semester_end, '
                       'sum(a.hours) AS hours '
                       'FROM semester s, training t, "group" g, attendance a '
                       'WHERE a.student_id = %s '
                       'AND a.training_id = t.id '
                       'AND t.group_id = g.id '
                       'AND g.semester_id = s.id '
                       'GROUP BY s.id', (student.pk,))
        return dictfetchall(cursor)


def get_detailed_hours(student: Student, semester: Semester):
    """
    Retrieves statistics of hours in one semester
    """
    with connection.cursor() as cursor:
        cursor.execute('SELECT g.name AS "group", t.start AS "timestamp", a.hours AS hours '
                       'FROM training t, "group" g, attendance a '
                       'WHERE a.student_id = %s '
                       'AND a.training_id = t.id '
                       'AND t.group_id = g.id '
                       'AND g.semester_id = %s', (student.pk, semester.pk))
        return dictfetchall(cursor)


def mark_hours(training: Training, student_hours: Iterable[Tuple[int, float]]):
    """
    Puts hours for one training session to one student. If hours for session were already put, updates it
    @param training: given training
    @param student_hours: iterable with items (<student_id:int>, <student_hours:float>)
    """
    for student_id, student_mark in student_hours:
        if student_id <= 0 or student_mark < 0.0:
            raise ValueError(f"All students id and marks must be non-negative, got {(student_id, student_mark)}")
        # Currently hours field is numeric(5,2), so
        # A field with precision 5, scale 2 must round to an absolute value less than 10^3.
        floor_max = 1000  # TODO: hardcoded limit
        if floor(student_mark) >= floor_max:
            raise ValueError(f"All students marks must floor to less than {floor_max}, "
                             f"got {student_mark} -> {floor(student_mark)} >= {floor_max}")
    with connection.cursor() as cursor:
        args_add_str = b",".join(
            cursor.mogrify("(%s, %s, %s)", (student_id, training.pk, student_mark))
            for student_id, student_mark in student_hours if student_mark > 0
        )
        args_del_str = b",".join(
            cursor.mogrify("(%s, %s)", (student_id, training.pk))
            for student_id, student_mark in student_hours if student_mark == 0
        )
        if len(args_add_str) > 0:
            cursor.execute(f'INSERT INTO attendance (student_id, training_id, hours) VALUES {args_add_str.decode()} '
                           f'ON CONFLICT ON CONSTRAINT unique_attendance '
                           f'DO UPDATE set hours=excluded.hours')
        if len(args_del_str) > 0:
            cursor.execute(f'DELETE FROM attendance '
                           f'WHERE  (student_id, training_id) IN ({args_del_str.decode()})')


def toggle_illness(student: Student):
    """
    Toggles student's illness
    """
    student.is_ill = not student.is_ill
    student.save()
