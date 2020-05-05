from typing import List, Tuple, Optional

from ..core.config import SC_TRAINERS_GROUP_NAME
from ..models.group import Group, EnrolledGroup
from ..models.sport import Sport


def __tuple_to_sport(row: Tuple[int, str, bool]) -> Sport:
    id, name, special = row
    return Sport(id=id, name=name, special=special)


def __tuple_to_group(row: Tuple[int, str, str, str, int, Optional[str], Optional[int], bool]) -> Group:
    """
    @param row - either 8 or 9 elements tuple, last element current_load is optional
    @return Group instance
    """
    id, name, sport_name, semester, capacity, description, trainer_id, is_club = row[:8]
    return Group(
        id=id,
        name=name,
        sport_name=sport_name,
        semester=semester,
        current_load=row[8] if len(row) == 9 else None,
        capacity=capacity,
        description=description,
        trainer_id=trainer_id,
        is_club=is_club
    )


def __tuple_to_enrolled_group(
        row: Tuple[int, str, str, str, int, Optional[str], Optional[int], bool, bool]
) -> EnrolledGroup:
    id, name, sport_name, semester, capacity, description, trainer_id, is_club, is_primary = row
    return EnrolledGroup(
        id=id,
        name=name,
        sport_name=sport_name,
        semester=semester,
        capacity=capacity,
        description=description,
        trainer_id=trainer_id,
        is_club=is_club,
        is_primary=is_primary
    )


def get_sports(conn, all=False) -> List[Sport]:
    """
    Retrieves existing sport types
    @param conn - Database connection
    @param all - If true, returns also special sport types
    @return list of all sport types
    """
    cursor = conn.cursor()
    if all:
        cursor.execute('SELECT id, name, special FROM sport')
    else:
        cursor.execute('SELECT id, name, special FROM sport WHERE special = FALSE')
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
    cursor.execute('SELECT id, name, special FROM sport WHERE id = %s', (sport_id,))
    row = cursor.fetchone()
    return __tuple_to_sport(row) if row else None


def get_groups(conn, clubs: Optional[bool] = None) -> List[Group]:
    """
    Retrieves existing groups
    @param conn - Database connection
    @param clubs - If None, returns all groups; if true, returns only clubs; if false, return only non-clubs
    @return list of all groups
    """
    cursor = conn.cursor()
    if clubs is None:
        cursor.execute(
            'SELECT g.id, g.name, sport.name, s.name, capacity, description, trainer_id, is_club, count(e.id) '
            'FROM sport, semester s, "group" g '
            'LEFT JOIN enroll e ON e.group_id = g.id '
            'WHERE s.id = current_semester() '
            'AND sport_id = sport.id '
            'AND semester_id = s.id '
            'GROUP BY g.id, sport.id, s.id')
    else:
        cursor.execute(
            'SELECT g.id, g.name, sport.name, s.name, capacity, description, trainer_id, is_club, count(e.id) '
            'FROM sport, semester s, "group" g '
            'LEFT JOIN enroll e ON e.group_id = g.id '
            'WHERE s.id = current_semester() '
            'AND sport_id = sport.id '
            'AND semester_id = s.id '
            'AND is_club = %s '
            'GROUP BY g.id, sport.id, s.id', (clubs,))
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


def get_student_groups(conn, student_id) -> List[EnrolledGroup]:
    """
    Retrieves groups, where student is enrolled
    @param conn - Database connection
    @param student_id - id of searched user
    @return number of enrolled students
    """
    cursor = conn.cursor()
    cursor.execute('SELECT g.id, g.name, sport.name, s.name, capacity, description, trainer_id, is_club, e.is_primary '
                   'FROM enroll e, "group" g, sport, semester s '
                   'WHERE s.id = current_semester() '
                   'AND sport_id = sport.id '
                   'AND semester_id = s.id '
                   'AND e.group_id = g.id '
                   'AND e.student_id = %s '
                   'ORDER BY e.is_primary DESC', (student_id,))
    rows = cursor.fetchall()
    return list(map(__tuple_to_enrolled_group, rows))


def get_training_groups(conn, trainer_id) -> List[Group]:
    """
    For a given trainer return all groups he/she is training in current semester

    :param conn: Database connection
    :param trainer_id: id of a trainer
    :return: list of group trainer is trainings in current semester
    """
    cursor = conn.cursor()
    cursor.execute(
        "select g.id, "
        "       g.name, "
        "       sp.name, "
        "       sem.name, "
        "       g.capacity, "
        "       g.description, "
        "       trainer_id, "
        "       is_club "
        'from "group" g '
        "         join sport sp on g.sport_id = sp.id "
        "         join semester sem on g.semester_id = sem.id "
        "where "
        "       sem.id = current_semester() "
        "       AND g.trainer_id = %s", (trainer_id,)
    )
    rows = cursor.fetchall()
    return list(map(__tuple_to_group, rows))


def get_sc_training_group(conn) -> Group:
    cursor = conn.cursor()
    cursor.execute('SELECT g.id, g.name, sport.name, s.name, capacity, description, trainer_id, is_club '
                   'FROM "group" g, sport, semester s '
                   'WHERE s.id = current_semester() '
                   'AND sport_id = sport.id '
                   'AND semester_id = s.id '
                   'AND g.name = %s', (SC_TRAINERS_GROUP_NAME,))
    row = cursor.fetchone()
    if row is None:
        raise ValueError("Unable to find SC training group")
    return __tuple_to_group(row)
