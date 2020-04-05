from datetime import datetime
from typing import List, Tuple

from ..models.training import Training


def __tuple_to_training(row: Tuple[int, datetime, datetime, int]) -> Training:
    id, start, end, group_id = row
    return Training(id=id, start=start, end=end, group_id=group_id)


def get_trainings(conn, group_id: int) -> List[Training]:
    """
    Retrieves existing training for given group
    @param conn - Database connection
    @param group_id - searched group id
    @return list of all sport types
    """
    cursor = conn.cursor()
    cursor.execute('SELECT id, "start", "end", group_id FROM training WHERE group_id = %s', (group_id,))
    rows = cursor.fetchall()
    return list(map(__tuple_to_training, rows))


def get_trainings_in_time(conn, sport_id: int, start: datetime, end: datetime) \
        -> List[Tuple[str, datetime, datetime, int, int]]:
    cursor = conn.cursor()
    cursor.execute('select g.name, t.start, t."end", g.capacity, g.id '
                   'from sport s '
                   'join "group" g on g.sport_id = s.id '
                   'join training t on t.group_id = g.id '
                   'where s.id = %s and t.start >= %s and t.end <= %s', (sport_id, start, end))
    rows = cursor.fetchall()
    return rows
