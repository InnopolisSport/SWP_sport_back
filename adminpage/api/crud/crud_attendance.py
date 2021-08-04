from math import floor
from typing import Iterable, Tuple, List
from typing_extensions import TypedDict

from django.db import connection

from api.crud.utils import dictfetchall
from sport.models import Student, Semester, Training

from api.crud.crud_semester import get_ongoing_semester
from sport.models import Attendance


class BriefHours(TypedDict):
    semester_id: int
    semester_name: str
    semester_start: str
    semester_end: str
    hours: int


def get_brief_hours(student: Student) -> List[BriefHours]:
    """
    Retrieves statistics of hours per different semesters
    """
    hours = get_student_hours(student)
    hours = [hours['ongoing_semester']] + hours['last_semesters_hours']

    brief_hours: List[BriefHours] = []
    for sem in hours:
        semester = Semester.objects.get(id=sem['id_sem'])
        element: BriefHours = {
            'semester_id': semester.id,
            'semester_name': semester.name,
            'semester_start': semester.start.strftime("%b. %d, %Y"),
            'semester_end': semester.end.strftime("%b. %d, %Y"),
            'hours': int(sem['hours_not_self'] + sem['hours_self_not_debt'] + sem['hours_self_debt'])
        }
        brief_hours.append(element)

    return brief_hours
    # with connection.cursor() as cursor:
    #     cursor.execute('SELECT '
    #                    's.id AS semester_id, '
    #                    's.name AS semester_name, '
    #                    's.start AS semester_start, '
    #                    's.end AS semester_end, '
    #                    'sum(a.hours) AS hours '
    #                    'FROM semester s, training t, "group" g, attendance a '
    #                    'WHERE a.student_id = %s '
    #                    'AND a.training_id = t.id '
    #                    'AND t.group_id = g.id '
    #                    'AND g.semester_id = s.id '
    #                    'GROUP BY s.id', (student.pk,))
    #     return dictfetchall(cursor)


def get_detailed_hours(student: Student, semester: Semester):
    """
    Retrieves statistics of hours in one semester
    """
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT g.name AS "group", t.custom_name AS custom_name, t.start AS "timestamp", a.hours AS hours '
            'FROM training t, "group" g, attendance a '
            'WHERE a.student_id = %s '
            'AND a.training_id = t.id '
            'AND t.group_id = g.id '
            'AND g.semester_id = %s '
            'ORDER BY t.start', (student.pk, semester.pk))
        return dictfetchall(cursor)


def get_detailed_hours_and_self(student: Student, semester: Semester):
    """
    Retrieves statistics of hours in one semester
    """
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT g.name AS "group", t.custom_name AS custom_name, t.start AS "timestamp", a.hours AS hours, true AS "approved" '
            'FROM training t, "group" g, attendance a, "self_sport_report" r '
            'WHERE a.student_id = %(student)s '
            'AND a.training_id = t.id '
            'AND t.group_id = g.id '
            'AND r.id = a.cause_report_id '
            'AND g.semester_id = %(semester)s '
            'UNION '
            'SELECT \'Self training\' AS "group", CONCAT(\'[Self] \', g.name) AS custom_name, r.uploaded as timestamp, r.hours, r.approval AS "approved" '
            'FROM "self_sport_report" r, "self_sport_group" g '
            'WHERE r.semester_id = %(semester)s '
            'AND r.student_id = %(student)s '
            'AND (r.approval IS NULL OR r.approval = false) '
            'AND g.id = r.training_type_id '
            'ORDER BY timestamp', {'student': student.pk, 'semester': semester.pk})
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


class SemesterHours(TypedDict):
    id_sem: int
    hours_not_self: float
    hours_self_not_debt: float
    hours_self_debt: float
    hours_sem_max: int


def get_student_hours(student_id, **kwargs) -> TypedDict('StudentHours',
                                                         {'last_semesters_hours': List[SemesterHours],
                                                          'ongoing_semester': SemesterHours}):
    student = Student.objects.get(user_id=student_id)
    sem_info_cur = {"id_sem": 0, "hours_not_self": 0.0, "hours_self_not_debt": 0.0,
                    "hours_self_debt": 0.0, "hours_sem_max": 0.0}

    query_attend_current_semester = Attendance.objects.filter(student_id=student_id,
                                                              training__group__semester=get_ongoing_semester())
    sem_info_cur['id_sem'] = get_ongoing_semester().id
    sem_info_cur['hours_sem_max'] = get_ongoing_semester().hours
    for i in query_attend_current_semester:
        if i.cause_report is None:
            sem_info_cur['hours_not_self'] += float(i.hours)
        elif i.cause_report.debt is True:
            sem_info_cur['hours_self_debt'] += float(i.hours)
        else:
            sem_info_cur['hours_self_not_debt'] += float(i.hours)

    sem_info = {"id_sem": 0, "hours_not_self": 0.0, "hours_self_not_debt": 0.0,
                "hours_self_debt": 0.0, "hours_sem_max": 0.0}
    last_sem_info_arr = []

    last_semesters = Semester.objects.filter(end__lt=get_ongoing_semester().start).order_by('-end')

    for i in last_semesters:
        if student in i.academic_leave_students.all():
            pass
        elif i.end.year >= student.enrollment_year:
            sem_info["id_sem"] = i.id
            sem_info["hours_sem_max"] = i.hours
            query_attend_last_semester = Attendance.objects.filter(student_id=student_id,
                                                                   training__group__semester=i)

            for j in query_attend_last_semester:
                if j.cause_report is None:
                    sem_info['hours_not_self'] += float(i.hours)
                elif j.cause_report.debt is True:
                    sem_info['hours_self_debt'] += float(i.hours)
                else:
                    sem_info['hours_self_not_debt'] += float(i.hours)

            last_sem_info_arr.append(sem_info)
            sem_info = {"id_sem": 0, "hours_not_self": 0.0, "hours_self_not_debt": 0.0,
                        "hours_self_debt": 0.0, "hours_sem_max": 0.0}
    return {
        "last_semesters_hours": last_sem_info_arr,
        "ongoing_semester": sem_info_cur
    }


def get_negative_hours(student_id, hours_info=None, **kwargs):
    student_hours = get_student_hours(student_id) if hours_info is None else hours_info
    sem_now = student_hours['ongoing_semester']
    res = 0.0
    for i in student_hours['last_semesters_hours']:
        res += i['hours_self_debt'] + min(i['hours_not_self'] + i['hours_self_not_debt'] - i['hours_sem_max'], 0)
    res += sem_now['hours_self_debt'] + sem_now['hours_not_self'] + sem_now['hours_self_not_debt']
    return res
