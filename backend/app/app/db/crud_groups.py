from typing import List, Tuple, Optional
from ..models.sport import Sport
from ..models.group import Group


def __tuple_to_sport(row: Tuple[int, str]) -> Sport:
    id, name = row
    return Sport(id=id, name=name)


def __tuple_to_group(row: Tuple[int, str, str, str, int, Optional[str], Optional[int]]) -> Group:
    id, name, sport_name, semester, capacity, description, trainer_id = row
    return Group(
        id=id,
        name=name,
        sport_name=sport_name,
        semester=semester,
        capacity=capacity,
        description=description,
        trainer_id=trainer_id
    )


def get_sports(conn) -> List[Sport]:
    """
    Retrieves existing sport types
    @param conn - Database connection
    @return list of all sport types
    """
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM sport')
    rows = cursor.fetchall()
    return list(map(__tuple_to_sport, rows))


def get_groups(conn) -> List[Group]:
    """
        Retrieves existing groups
        @param conn - Database connection
        @return list of all groups
        """
    cursor = conn.cursor()
    cursor.execute('SELECT g.id, g.name, sport.name, semester.name, capacity, description, trainer_id '
                   'FROM "group" g, sport, semester WHERE sport_id = sport.id AND semester_id = semester.id')
    rows = cursor.fetchall()
    return list(map(__tuple_to_group, rows))
