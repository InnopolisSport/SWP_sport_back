from django.db.models import F
from sport.models import Training

def dictfetchall(cursor):
    """Return all rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def dictfetchone(cursor):
    """Return one rows from a cursor as a dict"""
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    return dict(zip(columns, row)) if row is not None else None

def get_trainers(training_id: int):
    """
    Return the list of dictionaries containing trainers' information
    """
    query = Training.objects.filter(
        id=training_id,
    ).values(
        'group__trainers__first_name',
        'group__trainers__last_name',
        'group__trainers__email',
    ).annotate(
        trainer_first_name=F('group__trainers__first_name'),
        trainer_last_name=F('group__trainers__last_name'),
        trainer_email=F('group__trainers__email'),
    )

    return query