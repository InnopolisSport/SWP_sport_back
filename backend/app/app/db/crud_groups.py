from typing import List, Tuple
from app.db import conn


def create_sport(name: str):
    """
    Creates new sport type
    @param name: str - sport type name
    """
    cursor = conn.cursor()
    cursor.execute('INSERT INTO sport (name) VALUES (%s)', (name,))
    conn.commit()


def get_sports() -> List[Tuple[int, str]]:
    """
    Retrieves existing sport types
    @return list of tuples (sport_id, name)
    """
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM sport')
    return cursor.fetchall()


def delete_sport(sport_id: int):
    """
    Deletes existing sport type by its id
    @param sport_id: int - sport id
    """
    cursor = conn.cursor()
    cursor.execute('DELETE FROM sport WHERE id=%s', (sport_id,))
    conn.commit()


def create_group(name: str, sport_id: int, trainer_id: int = None):
    """
    Creates new sport group
    @param name: str - new sport group name
    @param sport_id: int - chosen sport type id
    @param trainer_id: int - assigned trainer id
    """
    cursor = conn.cursor()
    cursor.execute('INSERT INTO "group" (name, sport_id, trainer_id) VALUES (%s, %s, %s)', (name, sport_id, trainer_id))
    conn.commit()


def get_groups() -> List[Tuple[int, str, str, int]]:
    """
    Retrieves existing sport group
    @return list of tuples (group_id, group_name, sport_name, trainer_id)
    """
    cursor = conn.cursor()
    cursor.execute('SELECT g.id, g.name, s.name, g.trainer_id FROM "group" g JOIN sport s ON g.sport_id = s.id')
    return cursor.fetchall()


def delete_group(group_id: int):
    """
    Deletes existing group by its id
    @param group_id: int - group id
    """
    cursor = conn.cursor()
    cursor.execute('DELETE FROM "group" WHERE id=%s', (group_id,))
    conn.commit()
