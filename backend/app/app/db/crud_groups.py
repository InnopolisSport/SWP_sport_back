from typing import List, Tuple, Optional

from ..models.group import Group
from ..models.sport import Sport


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


def get_sport_by_id(conn, sport_id: int) -> Optional[Sport]:
    """
    Retrieves sport by id if any
    @param conn - Database connection
    @param sport_id - An id of sport you want to retrieve
    @return Sport if sport with given id is present, None otherwise
    """
    cursor = conn.cursor()
    cursor.execute('SELECT id, name FROM sport WHERE id = %s', (sport_id,))
    row = cursor.fetchone()
    return __tuple_to_sport(row) if row else None


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


def get_current_load(conn, group_id: int) -> int:
    """
    Retrieves number of enrolled students in a group
    @param conn - Database connection
    @param group_id - id of searched group
    @return number of enrolled students
    """
    cursor = conn.cursor()
    cursor.execute('SELECT count(*) FROM enroll WHERE group_id = %s', (group_id,))
    count = cursor.fetchone()[0]
    return count


def get_student_main_group(conn, student_id) -> Group:
    """
    Retrieves current primary group, where student is enrolled
    @param conn - Database connection
    @param student_id - id of searched user
    @return number of enrolled students
    """
    cursor = conn.cursor()
    cursor.execute('SELECT g.id, g.name, sport.name, semester.name, capacity, description, trainer_id '
                   'FROM enroll e, "group" g, sport, semester '
                   'WHERE sport_id = sport.id '
                   'AND semester_id = semester.id '
                   'AND e.group_id = g.id '
                   'AND e.student_id = %s', (student_id,))
    row = cursor.fetchone()
    return __tuple_to_group(row) if row is not None else None
