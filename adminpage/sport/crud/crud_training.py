from datetime import datetime
from django.db import connection

from sport.crud import dictfetchone, dictfetchall
from sport.models import Student, Trainer


def get_attended_training_info(training_id: int, student: Student):
    """
    Retrieves more detailed training info by its id
    @param training_id - searched training id
    @param student - request sender student
    @return found training
    """
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT '
            'g.id AS group_id, '
            'g.name AS group_name, '
            'g.description AS group_description, '
            'tc.name AS training_class, '
            'g.capacity AS capacity, '
            'count(e.id) AS current_load, '
            'd.first_name AS trainer_first_name, '
            'd.last_name AS trainer_last_name, '
            'd.email AS trainer_email, '
            'a.hours AS hours, '
            'exists(SELECT true FROM enroll e WHERE e.group_id = g.id AND e.student_id = %s) AS is_enrolled, '
            'exists(SELECT true FROM enroll e WHERE e.group_id = g.id AND e.student_id = %s AND is_primary = TRUE) AS is_primary '
            'FROM training tr '
            'LEFT JOIN training_class tc ON tr.training_class_id = tc.id, "group" g '
            'LEFT JOIN enroll e ON e.group_id = g.id '
            'LEFT JOIN trainer t ON t.id = g.trainer_id '
            'LEFT JOIN auth_user d ON t.user_id = d.id '
            'LEFT JOIN attendance a ON a.training_id = %s AND a.student_id = %s '
            'WHERE tr.group_id = g.id '
            'AND tr.id = %s '
            'GROUP BY g.id, d.id, t.id, a.id, tc.id', (student.pk, student.pk, training_id, student.pk, training_id))
        return dictfetchone(cursor)


def get_group_info(group_id: int, student: Student):
    """
    Retrieves more detailed group info by its id
    @param group_id - searched group id
    @param student - request sender student
    @return found group
    """
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT '
            'g.id AS group_id, '
            'g.name AS group_name, '
            'g.description AS group_description, '
            'g.capacity AS capacity, '
            'count(e.id) AS current_load, '
            'd.first_name AS trainer_first_name, '
            'd.last_name AS trainer_last_name, '
            'd.email AS trainer_email, '
            'exists(SELECT true FROM enroll e WHERE e.group_id = %s AND e.student_id = %s) AS is_enrolled, '
            'exists(SELECT true FROM enroll e WHERE e.group_id = %s AND e.student_id = %s AND is_primary = TRUE) AS is_primary '
            'FROM "group" g '
            'LEFT JOIN enroll e ON e.group_id = %s '
            'LEFT JOIN trainer t ON t.id = g.trainer_id '
            'LEFT JOIN auth_user d ON t.user_id = d.id '
            'WHERE g.id = %s '
            'GROUP BY g.id, t.id, d.id', (group_id, student.pk, group_id, student.pk, group_id, group_id))
        return dictfetchone(cursor)


def get_trainings_for_student(student: Student, start: datetime, end: datetime):
    """
    Retrieves existing trainings in the given range for given student
    @param student - searched student
    @param start - range start date
    @param end - range end date
    @return list of trainings for student
    """
    with connection.cursor() as cursor:
        cursor.execute('SELECT '
                       't.id AS id, '
                       't.start AS start, '
                       't."end" AS "end", '
                       'g.id AS group_id, '
                       'g.name AS group_name, '
                       'tc.name AS training_class, '
                       'a.hours AS hours '
                       'FROM enroll e, "group" g, training t '
                       'LEFT JOIN attendance a ON a.student_id = %s AND a.training_id = t.id '
                       'LEFT JOIN training_class tc ON t.training_class_id = tc.id '
                       'WHERE t.start > %s AND t."end" < %s '
                       'AND t.group_id = g.id '
                       'AND e.group_id = g.id '
                       'AND e.student_id = %s '
                       'AND g.semester_id = current_semester()', (student.pk, start, end, student.pk))
        return dictfetchall(cursor)


def get_trainings_for_trainer(trainer: Trainer, start: datetime, end: datetime):
    """
    Retrieves existing trainings in the given range for given student
    @param trainer - searched trainer
    @param start - range start date
    @param end - range end date
    @return list of trainings for student
    """
    with connection.cursor() as cursor:
        cursor.execute('SELECT '
                       't.id AS id, '
                       't.start AS start, '
                       't."end" AS "end", '
                       'g.id AS group_id, '
                       'g.name AS group_name, '
                       'tc.name AS training_class '
                       'FROM "group" g, training t LEFT JOIN training_class tc ON t.training_class_id = tc.id '
                       'WHERE t.start > %s AND t."end" < %s '
                       'AND t.group_id = g.id '
                       'AND g.trainer_id = %s '
                       'AND g.semester_id = current_semester()', (start, end, trainer.pk))
        return dictfetchall(cursor)


def get_trainings_in_time(sport_id: int, start: datetime, end: datetime):
    """
    Retrieves existing trainings in the given range for given sport type
    @param sport_id - searched sport id
    @param start - range start date
    @param end - range end date
    @return list of trainings info
    """
    with connection.cursor() as cursor:
        cursor.execute('SELECT '
                       'g.id AS group_id, '
                       'g.name AS group_name, '
                       'count(e.id) AS current_load, '
                       'g.capacity AS capacity, '
                       't.id AS id, '
                       't.start AS start, '
                       't."end" AS "end", '
                       'tc.name AS training_class '
                       'FROM sport sp, "group" g LEFT JOIN enroll e ON e.group_id = g.id, training t '
                       'LEFT JOIN training_class tc ON t.training_class_id = tc.id '
                       'WHERE g.sport_id = sp.id '
                       'AND g.semester_id = current_semester() '
                       'AND t.group_id = g.id '
                       'AND sp.id = %s '
                       'AND t.start >= %s '
                       'AND t.end <= %s '
                       'GROUP BY g.id, t.id, tc.id', (sport_id, start, end))
        return dictfetchall(cursor)


def get_students_grades(training_id: int):
    """
    Retrieves student grades for specific training
    @param training_id - searched training id
    @return list of student grades
    """
    with connection.cursor() as cursor:
        cursor.execute('SELECT '
                       's.id AS student_id, '
                       'd.first_name AS first_name, '
                       'd.last_name AS last_name, '
                       'd.email AS email, '
                       'a.hours AS hours '
                       'FROM training t, student s, attendance a, auth_user d '
                       'WHERE a.student_id = s.id '
                       'AND s.user_id = d.id '
                       'AND a.training_id = %s '
                       'AND s.is_ill = FALSE '
                       'AND t.id = %s '
                       'UNION DISTINCT '
                       'SELECT '
                       's.id AS student_id, '
                       'd.first_name AS first_name, '
                       'd.last_name AS last_name, '
                       'd.email AS email, '
                       'a.hours AS hours '
                       'FROM training t, enroll e, auth_user d, student s '
                       'LEFT JOIN attendance a ON a.student_id = s.id AND a.training_id = %s '
                       'WHERE s.id = e.student_id '
                       'AND s.user_id = d.id '
                       'AND s.is_ill = FALSE '
                       'AND t.id = %s '
                       'AND t.group_id = e.group_id ', (training_id, training_id, training_id, training_id))
        return dictfetchall(cursor)
