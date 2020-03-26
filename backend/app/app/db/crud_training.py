from typing import List, Tuple
from ..models.training import Training
from datetime import datetime


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
