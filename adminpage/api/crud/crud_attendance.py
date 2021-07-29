from math import floor
from typing import Iterable, Tuple

from django.db import connection

from api.crud.utils import dictfetchall
from sport.models import Student, Semester, Training

from api.crud.crud_semester import get_ongoing_semester
from sport.models import Attendance


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
        cursor.execute('SELECT g.name AS "group", t.custom_name AS custom_name, t.start AS "timestamp", a.hours AS hours '
                       'FROM training t, "group" g, attendance a '
                       'WHERE a.student_id = %s '
                       'AND a.training_id = t.id '
                       'AND t.group_id = g.id '
                       'AND g.semester_id = %s '
                       'ORDER BY t.start', (student.pk, semester.pk))
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


class Response:
    pass


def get_student_hours(student_id, **kwargs):
    hours_current_sem = {"hours_not_self_current": 0.0, "hours_self_not_debt_current": 0.0, "hours_self_debt_current": 0.0}
    hours_last_sem = {"hours_not_self_last": 0.0, "hours_self_not_debt_last": 0.0, "hours_self_debt_last": 0.0}
    last_semesters = Semester.objects.filter(end__lt=get_ongoing_semester().start).order_by('-end')

    query_attend_current_semester = Attendance.objects.filter(student_id=student_id,
                                                              training__group__semester=get_ongoing_semester())
    print(get_ongoing_semester())
    query_attend_last_semester = Attendance.objects.filter(student_id=student_id,
                                                           training__group__semester=last_semesters[0]) if len(last_semesters) != 0 else []
    for i in query_attend_current_semester:
        if i.cause_report is None:
            hours_current_sem['hours_not_self_current'] += float(i.hours)
        elif i.cause_report.debt is True:
            hours_current_sem['hours_self_debt_current'] += float(i.hours)
        else:
            hours_current_sem['hours_self_not_debt_current'] += float(i.hours)

    for i in query_attend_last_semester:
        if i.cause_report is None:
            hours_last_sem['hours_not_self_last'] += float(i.hours)
        elif i.cause_report.debt is True:
            hours_last_sem['hours_self_debt_last'] += float(i.hours)
        else:
            hours_last_sem['hours_self_not_debt_last'] += float(i.hours)
    return {
        "hours_not_self_current": hours_current_sem['hours_not_self_current'],
        "hours_self_not_debt_current": hours_current_sem['hours_self_not_debt_current'],
        "hours_self_debt_current": hours_current_sem['hours_self_debt_current'],
        "hours_sem_max_current": get_ongoing_semester().hours,
        "hours_not_self_last": hours_last_sem['hours_not_self_last'],
        'hours_self_not_debt_last': hours_last_sem['hours_self_not_debt_last'],
        "hours_self_debt_last": hours_last_sem['hours_self_debt_last'],
        "hours_sem_max_last": last_semesters[0]['hours'] if len(last_semesters) != 0 else 0
    }
