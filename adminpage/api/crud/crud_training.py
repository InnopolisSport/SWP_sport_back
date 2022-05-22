from datetime import datetime, timedelta
from django.utils import timezone

from django.conf import settings
from django.db import connection
from django.db.models import Q, F

from api.crud.utils import dictfetchone, dictfetchall, get_trainers, get_trainers_group
from api.crud.crud_semester import get_ongoing_semester
from sport.models import Student, Trainer, Group, Training, Sport, TrainingCheckIn


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
            'tr.custom_name AS custom_name, '
            'g.description AS group_description, '
            'g.link_name AS link_name, '
            'g.link AS link, '
            'tc.name AS training_class, '
            'g.capacity AS capacity, '
            'count(e.id) AS current_load, '
            'd.first_name AS trainer_first_name, '
            'd.last_name AS trainer_last_name, '
            'd.email AS trainer_email, '
            'COALESCE(a.hours, 0) AS hours, '
            'COALESCE(bool_or(e.student_id = %(student_pk)s), false) AS is_enrolled '
            'FROM training tr '
            'LEFT JOIN training_class tc ON tr.training_class_id = tc.id, "group" g '
            'LEFT JOIN enroll e ON e.group_id = g.id '
            'LEFT JOIN auth_user d ON g.trainer_id = d.id '
            'LEFT JOIN attendance a ON a.training_id = %(training_pk)s AND a.student_id = %(student_pk)s '
            'WHERE tr.group_id = g.id '
            'AND tr.id = %(training_pk)s '
            'GROUP BY g.id, d.id, a.id, tc.id, tr.id',
            {
                "student_pk": student.pk,
                "training_pk": training_id
            }
        )

        info = dictfetchone(cursor)
        info['trainers'] = get_trainers(training_id)

        return info


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
            'g.link_name AS link_name, '
            'g.link AS link, '
            'g.capacity AS capacity, '
            'g.is_club AS is_club, '
            'count(e.id) AS current_load, '
            'd.first_name AS trainer_first_name, '
            'd.last_name AS trainer_last_name, '
            'd.email AS trainer_email, '
            'COALESCE(bool_or(e.student_id = %(student_id)s), false) AS is_enrolled '
            'FROM "group" g '
            'LEFT JOIN enroll e ON e.group_id = %(group_id)s '
            'LEFT JOIN auth_user d ON g.trainer_id = d.id '
            'WHERE g.id = %(group_id)s '
            'GROUP BY g.id, d.id', {"group_id": group_id, "student_id": student.pk})

        info = dictfetchone(cursor)
        info['trainers'] = get_trainers_group(group_id)

        info['can_enroll'] = student.sport is not None and \
                             student.sport==Group.objects.get(id=info['group_id']).sport and \
                             not Group.objects.filter(enrolls__student=student,
                                                      semester=get_ongoing_semester()).exists()

        return info


def can_check_in(student: Student, training: Training):
    return student.medical_group in training.group.allowed_medical_groups.all() \
           and TrainingCheckIn.objects.filter(student=student, training__start__day=training.start.day).count() < 2 \
           and TrainingCheckIn.objects.filter(student=student, training__start__day=training.start.day,
                                              training__group__sport=training.group.sport).count() < 1 \
           and training.start < (timezone.now() + timedelta(days=7)) \
           and training.end > timezone.now()



# TODO: Rewrite
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
                       'FALSE AS can_grade '
                       'FROM enroll e, "group" g, sport s, training t '
                       'LEFT JOIN training_class tc ON t.training_class_id = tc.id '
                       'WHERE ((t.start > %(start)s AND t.start < %(end)s) '
                       'OR (t."end" > %(start)s AND t."end" < %(end)s) '
                       'OR (t.start < %(start)s AND t."end" > %(end)s)) '
                       'AND g.sport_id = s.id '
                       'AND s.name != %(extra_sport)s '
                       'AND t.group_id = g.id '
                       'AND e.student_id = %(student_id)s '
                       'AND g.semester_id = current_semester() '
                       'UNION DISTINCT '
                       'SELECT '
                       't.id AS id, '
                       't.start AS start, '
                       't."end" AS "end", '
                       'g.id AS group_id, '
                       'COALESCE(t.custom_name, g.name) AS group_name, '
                       'tc.name AS training_class, '
                       'FALSE AS can_grade '
                       'FROM attendance a, "group" g, training t '
                       'LEFT JOIN training_class tc ON t.training_class_id = tc.id '
                       'WHERE ((t.start > %(start)s AND t.start < %(end)s) OR (t."end" > %(start)s AND t."end" < %(end)s) OR (t.start < %(start)s AND t."end" > %(end)s)) '
                       'AND a.student_id = %(student_id)s '
                       'AND t.group_id = g.id '
                       'AND a.training_id = t.id '
                       'AND g.semester_id = current_semester()',
                       {"start": start, "end": end, "extra_sport": settings.OTHER_SPORT_NAME, "student_id": student.pk}
                       )
        d = dictfetchall(cursor)
        for e in d:
            t = Training.objects.get(pk=e['id'])
            e['can_check_in'] = can_check_in(student, t)
            e['checked_in'] = t.checkins.filter(student=student).exists()
        return d


def get_trainings_for_trainer(trainer: Trainer, start: datetime, end: datetime):
    """
    Retrieves existing trainings in the given range for given student
    @param trainer - searched trainer
    @param start - range start date
    @param end - range end date
    @return list of trainings for trainer
    """
    query = Training.objects.select_related(
        'group',
        'training_class',
    ).filter(
        Q(group__semester__id=get_ongoing_semester().id) &
        Q(group__trainers=trainer) & (
                Q(start__gt=start) & Q(start__lt=end) |
                Q(end__gt=start) & Q(end__lt=end) |
                Q(start__lt=start) & Q(end__gt=end)
        )
    ).values(
        'id',
        'start',
        'end',
        'group_id',
        'group__name',
        'training_class__name',
    ).annotate(
        group_name=F('group__name'),
        training_class=F('training_class__name'),
    ).values(
        'id',
        'start',
        'end',
        'group_id',
        'group_name',
        'training_class',
    )

    for entry in query:
        entry["can_grade"] = True

    return list(query)


def get_students_grades(training_id: int):
    """
    Retrieves student grades for specific training
    @param training_id - searched training id
    @return list of student grades
    """
    with connection.cursor() as cursor:
        cursor.execute('SELECT '
                       'd.id AS student_id, '
                       'd.first_name AS first_name, '
                       'd.last_name AS last_name, '
                       'd.email AS email, '
                       'a.hours AS hours, '
                       'm.name AS med_group, '
                       'concat(d.first_name, \' \', d.last_name) as full_name '
                       'FROM training t, attendance a, auth_user d, student s '
                       'LEFT JOIN medical_group m ON m.id = s.medical_group_id '
                       'WHERE s.user_id = a.student_id '
                       'AND d.id = a.student_id '
                       'AND a.training_id = %(training_id)s '
                       'AND t.id = %(training_id)s '
                       'UNION DISTINCT '
                       'SELECT '
                       'd.id AS student_id, '
                       'd.first_name AS first_name, '
                       'd.last_name AS last_name, '
                       'd.email AS email, '
                       'COALESCE(a.hours, 0) AS hours, '
                       'm.name AS med_group, '
                       'concat(d.first_name, \' \', d.last_name) as full_name '
                       'FROM training t, sport_trainingcheckin e, auth_user d, student s '
                       'LEFT JOIN attendance a ON a.student_id = s.user_id AND a.training_id = %(training_id)s '
                       'LEFT JOIN medical_group m ON m.id = s.medical_group_id '
                       'WHERE s.user_id = e.student_id '
                       'AND d.id = e.student_id '
                       'AND t.id = %(training_id)s '
                       'AND t.id = e.training_id ', {"training_id": training_id})
        return dictfetchall(cursor)


def get_student_last_attended_dates(group_id: int):
    """
    Retrieves last attended dates for students
    @param group_id - searched group id
    @return list of students and their last attended training timestamp
    """
    with connection.cursor() as cursor:
        cursor.execute('SELECT '
                       'd.id AS student_id, '
                       'd.first_name AS first_name, '
                       'd.last_name AS last_name, '
                       'd.email AS email, '
                       'max(t.start) AS last_attended, '
                       'concat(d.first_name, \' \', d.last_name) as full_name '
                       'FROM enroll e, auth_user d '
                       'LEFT JOIN attendance a ON a.student_id = d.id '
                       'LEFT JOIN training t ON a.training_id = t.id AND t.group_id = %(group_id)s '
                       'WHERE e.group_id = %(group_id)s '
                       'AND e.student_id = d.id '
                       'GROUP BY d.id', {"group_id": group_id})
        return dictfetchall(cursor)
