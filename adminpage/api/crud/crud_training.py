from datetime import datetime, timedelta

from django.conf import settings
from django.db import connection
from django.db.models import Q, Sum
from django.utils import timezone

from api.crud.crud_semester import get_ongoing_semester
from api.crud.utils import dictfetchone, dictfetchall, get_trainers_group
from sport.models import Student, Trainer, Group, Training, TrainingCheckIn


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
    time_now = timezone.now()

    all_checkins = TrainingCheckIn.objects.filter(
        student=student,
        training__start__date=training.start.date()
    )
    same_type_checkins = TrainingCheckIn.objects.filter(
        student=student,
        training__group__sport=training.group.sport,
        training__start__date=training.start.date()
    )

    total_hours = sum(c.training.academic_duration for c in all_checkins)
    same_type_hours = sum(c.training.academic_duration for c in same_type_checkins)

    conditions = [
        student.medical_group in training.group.allowed_medical_groups.all(),
        total_hours + training.academic_duration <= 4,
        same_type_hours + training.academic_duration <= 2,
        training.start < (time_now + timedelta(days=7)),
        time_now < training.end
    ]

    return all(conditions)


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
                       'FROM "group" g, sport s, training t '
                       'LEFT JOIN training_class tc ON t.training_class_id = tc.id '
                       'WHERE ((t.start > %(start)s AND t.start < %(end)s) '
                       'OR (t."end" > %(start)s AND t."end" < %(end)s) '
                       'OR (t.start < %(start)s AND t."end" > %(end)s)) '
                       'AND g.sport_id = s.id '
                       'AND s.name != %(extra_sport)s '
                       'AND t.group_id = g.id '
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
            e['group_name'] = t.group.to_frontend_name()

        return d


def get_trainings_for_trainer(trainer: Trainer, start: datetime, end: datetime):
    """
    Retrieves existing trainings in the given range for given student
    @param trainer - searched trainer
    @param start - range start date
    @param end - range end date
    @return list of trainings for trainer
    """
    trainings = Training.objects.select_related(
        'group',
        'training_class',
    ).filter(
        Q(group__semester__id=get_ongoing_semester().id) &
        Q(group__trainers=trainer) & (
                Q(start__gt=start) & Q(start__lt=end) |
                Q(end__gt=start) & Q(end__lt=end) |
                Q(start__lt=start) & Q(end__gt=end)
        )
    )
    return [{
        'id': e.id,
        'start': e.start,
        'end': e.end,
        'group_id': e.group_id,
        'group_name': e.group.to_frontend_name(),
        'training_class': e.training_class.name if e.training_class else None,
        'can_grade': True,
    } for e in trainings]


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
