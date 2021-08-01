from typing import Optional

from django.conf import settings
from django.db import connection
from django.db.models import F

import api.crud
from api.crud.utils import dictfetchall
from api.crud.crud_semester import get_ongoing_semester
from sport.models import Sport, Student, Trainer, Group


def get_sports(all=False, student: Optional[Student] = None):
    """
    Retrieves existing sport types
    @param all - If true, returns also special sport types
    @param student - if student passed, get sports applicable for student
    @return list of all sport types
    """

    if student is None or student.medical_group_id > 0:
        groups = Group.objects.filter(minimum_medical_group_id__gt=0, semester__pk=api.crud.get_ongoing_semester().pk)
    elif student.medical_group_id < 0:
        groups = Group.objects.filter(minimum_medical_group_id__lt=0, semester__pk=api.crud.get_ongoing_semester().pk)
    else:
        groups = Group.objects.filter(minimum_medical_group_id=0, semester__pk=api.crud.get_ongoing_semester().pk)

    # w/o distinct returns a lot of duplicated
    sports = Sport.objects.filter(id__in=groups.values_list('sport')).distinct()
    if not all:
        sports = sports.filter(special=False)

    sports_list = []
    for sport in sports.all().values():
        sport_groups = groups.filter(sport=sport['id'])

        trainers = set()
        for group_trainers in sport_groups.values_list('trainer'):
            trainers |= set(group_trainers)
        trainers = list(map(lambda t: Trainer.objects.get(user_id=t), trainers))

        sport['trainers'] = trainers
        sport['num_of_groups'] = sport_groups.count()

        sports_list.append(sport)

    return sports_list


def get_clubs(student: Optional[Student] = None):
    """
    Retrieves existing clubs
    @return list of all club
    """
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT '
            'g.id AS id, '
            'g.name AS name, '
            'sport.name AS sport_name, '
            's.name AS semester, '
            'capacity, description, trainer_id, is_club, '
            'count(e.id) AS current_load '
            'FROM sport, semester s, "group" g '
            'LEFT JOIN enroll e ON e.group_id = g.id '
            'WHERE s.id = current_semester() '
            'AND sport_id = sport.id '
            'AND semester_id = s.id '
            'AND is_club = TRUE '
            'AND sign(%(medical_group_id_sign)s) = sign(g.minimum_medical_group_id) '
            'GROUP BY g.id, sport.id, s.id', {
                "medical_group_id_sign": 1 if student is None else student.medical_group_id
            })
        return dictfetchall(cursor)


def get_student_groups(student: Student):
    """
    Retrieves groups, where student is enrolled
    @return list of group dicts
    """
    with connection.cursor() as cursor:
        cursor.execute('SELECT '
                       'g.id AS id, '
                       'g.name AS name, '
                       's.name AS sport_name '
                       'FROM enroll e, "group" g, sport s '
                       'WHERE g.semester_id = current_semester() '
                       'AND e.group_id = g.id '
                       'AND e.student_id = %s '
                       'AND s.id = g.sport_id ', (student.pk,))
        return dictfetchall(cursor)


def get_trainer_groups(trainer: Trainer):
    """
    For a given trainer return all groups he/she is training in current semester
    @return list of group trainer is trainings in current semester
    """
    # with connection.cursor() as cursor:
    #     cursor.execute('SELECT '
    #                    'g.id AS id, '
    #                    'g.name AS name, '
    #                    's.name AS sport_name '
    #                    'FROM "group" g, sport s '
    #                    'WHERE g.semester_id = current_semester() '
    #                    'AND g.sport_id = s.id '
    #                    'AND g.trainer_id = %s', (trainer.pk,))
    #     return dictfetchall(cursor)

    query = Group.objects.filter(
        semester__id=get_ongoing_semester().id,
        trainers__pk=trainer.pk,
    ).values(
        'id',
        'name',
        'sport',
    ).annotate(
        sport_name=F('sport'),

    )
    return query
    # Currently query is a list of one dictionary
    # Will it be converted to a dictionary?
