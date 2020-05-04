from datetime import datetime
from typing import List, Tuple

from ..models.training import Training, TrainingGrade, TrainingInfo, AttendedTrainingInfo, GroupInfo


def __tuple_to_training(row: Tuple[int, datetime, datetime, int, str, str, float]) -> Training:
    id, start, end, group_id, group_name, training_class, hours = row
    return Training(
        id=id,
        group_id=group_id,
        start=start,
        end=end,
        group_name=group_name,
        training_class=training_class,
        hours=hours
    )


def __tuple_to_training_for_trainer(row: Tuple[int, datetime, datetime, int, str, str]) -> Training:
    id, start, end, group_id, group_name, training_class = row
    return Training(
        id=id,
        group_id=group_id,
        start=start,
        end=end,
        group_name=group_name,
        training_class=training_class,
        can_grade=True
    )


def __tuple_to_training_extended(row: Tuple[int, str, int, int, int, datetime, datetime, str]) -> Training:
    group_id, group_name, current_load, capacity, id, start, end, training_class = row
    return Training(
        id=id,
        group_id=group_id,
        start=start,
        end=end,
        group_name=group_name,
        training_class=training_class,
        current_load=current_load,
        capacity=capacity
    )


def __tuple_to_training_info(row: Tuple[str, datetime, datetime, int]) -> TrainingInfo:
    group_name, start, end, trainer_id = row
    return TrainingInfo(
        group_name=group_name,
        start=start,
        end=end,
        trainer_id=trainer_id,
    )


def __tuple_to_attended_training_info(
        row: Tuple[int, str, str, int, int, str, str, str, float, bool, bool]) -> AttendedTrainingInfo:
    group_id, group_name, group_description, capacity, current_load, trainer_first_name, trainer_last_name, trainer_email, hours, is_enrolled, is_primary = row
    return AttendedTrainingInfo(
        group_id=group_id,
        group_name=group_name,
        group_description=group_description if group_description is not None else '',
        trainer_first_name=trainer_first_name,
        trainer_last_name=trainer_last_name,
        trainer_email=trainer_email,
        hours=hours if hours is not None else 0,
        is_enrolled=is_enrolled,
        capacity=capacity,
        current_load=current_load,
        is_primary=is_primary
    )


def __tuple_to_group_info(row: Tuple[int, str, str, int, int, str, str, str, bool, bool]) -> GroupInfo:
    group_id, group_name, group_description, capacity, current_load, trainer_first_name, trainer_last_name, trainer_email, is_enrolled, is_primary = row
    return GroupInfo(
        group_id=group_id,
        group_name=group_name,
        group_description=group_description if group_description is not None else '',
        trainer_first_name=trainer_first_name,
        trainer_last_name=trainer_last_name,
        trainer_email=trainer_email,
        is_enrolled=is_enrolled,
        capacity=capacity,
        current_load=current_load,
        is_primary=is_primary
    )


def __tuple_to_training_grade(row: Tuple[int, str, str, str, float]) -> TrainingGrade:
    student_id, first_name, last_name, email, hours = row
    return TrainingGrade(
        student_id=student_id,
        full_name=f'{first_name} {last_name}',
        email=email,
        hours=hours if hours is not None else 0
    )


def get_training_info(conn, training_id: int) -> TrainingInfo:
    """
    Retrieves training by its id
    @param conn - Database connection
    @param training_id - graded training id
    @return found training
    """
    cursor = conn.cursor()
    cursor.execute('SELECT g.name, t.start, t."end", g.trainer_id  '
                   'FROM training t, "group" g '
                   'WHERE t.group_id = g.id AND t.id = %s', (training_id,))
    return __tuple_to_training_info(cursor.fetchone())


def get_attended_training_info(conn, training_id: int, student_id: int) -> AttendedTrainingInfo:
    """
    Retrieves more detailed training info by its id
    @param conn - Database connection
    @param training_id - searched training id
    @param student_id - request sender student id
    @return found training
    """
    cursor = conn.cursor()
    cursor.execute(
        'SELECT g.id, g.name, g.description, g.capacity, count(e.id), t.first_name, t.last_name, t.email, a.hours, '
        'exists(SELECT true FROM enroll e WHERE e.group_id = g.id AND e.student_id = %s), '
        'exists(SELECT true FROM enroll e WHERE e.group_id = g.id AND e.student_id = %s AND is_primary = true) '
        'FROM training tr, "group" g '
        'LEFT JOIN enroll e ON e.group_id = g.id '
        'LEFT JOIN trainer t ON t.id = g.trainer_id '
        'LEFT JOIN attendance a ON a.training_id = %s AND a.student_id = %s '
        'WHERE tr.group_id = g.id '
        'AND tr.id = %s '
        'GROUP BY g.id, t.id, a.id', (student_id, student_id, training_id, student_id, training_id))
    return __tuple_to_attended_training_info(cursor.fetchone())


def get_group_info(conn, group_id: int, student_id: int) -> GroupInfo:
    """
    Retrieves more detailed group info by its id
    @param conn - Database connection
    @param group_id - searched group id
    @param student_id - request sender student id
    @return found training
    """
    cursor = conn.cursor()
    cursor.execute(
        'SELECT g.id, g.name, g.description, g.capacity, count(e.id), t.first_name, t.last_name, t.email, '
        'exists(SELECT true FROM enroll e WHERE e.group_id = %s AND e.student_id = %s), '
        'exists(SELECT true FROM enroll e WHERE e.group_id = %s AND e.student_id = %s AND is_primary = true) '
        'FROM "group" g '
        'LEFT JOIN enroll e ON e.group_id = %s '
        'LEFT JOIN trainer t ON t.id = g.trainer_id '
        'WHERE g.id = %s '
        'GROUP BY g.id, t.id', (group_id, student_id, group_id, student_id, group_id, group_id))
    return __tuple_to_group_info(cursor.fetchone())


def get_trainings_for_student(conn, student_id: int, start: datetime, end: datetime) -> List[Training]:
    """
    Retrieves existing trainings in the given range for given student
    @param conn - Database connection
    @param student_id - searched student id
    @param start - range start date
    @param end - range end date
    @return list of trainings for student
    """
    cursor = conn.cursor()
    cursor.execute('SELECT t.id, t.start, t."end", g.id, g.name, tc.name, a.hours '
                   'FROM enroll e, "group" g, training t '
                   'LEFT JOIN attendance a ON a.student_id = %s AND a.training_id = t.id '
                   'LEFT JOIN training_class tc ON t.training_class_id = tc.id '
                   'WHERE t.start > %s AND t."end" < %s '
                   'AND t.group_id = g.id '
                   'AND e.group_id = g.id '
                   'AND e.student_id = %s '
                   'AND g.semester_id = current_semester()', (student_id, start, end, student_id))
    rows = cursor.fetchall()
    return list(map(__tuple_to_training, rows))


def get_trainings_for_trainer(conn, trainer_id: int, start: datetime, end: datetime) -> List[Training]:
    """
    Retrieves existing trainings in the given range for given student
    @param conn - Database connection
    @param trainer_id - searched trainer id
    @param start - range start date
    @param end - range end date
    @return list of trainings for student
    """
    cursor = conn.cursor()
    cursor.execute('SELECT t.id, t.start, t."end", g.id, g.name, tc.name '
                   'FROM "group" g, training t LEFT JOIN training_class tc ON t.training_class_id = tc.id '
                   'WHERE t.start > %s AND t."end" < %s '
                   'AND t.group_id = g.id '
                   'AND g.trainer_id = %s '
                   'AND g.semester_id = current_semester()', (start, end, trainer_id))
    rows = cursor.fetchall()
    return list(map(__tuple_to_training_for_trainer, rows))


def get_trainings_in_time(conn, sport_id: int, start: datetime, end: datetime) \
        -> List[Training]:
    cursor = conn.cursor()
    cursor.execute('SELECT g.id, g.name, count(e.id), g.capacity, t.id, t.start, t."end", tc.name '
                   'FROM sport sp, "group" g LEFT JOIN enroll e ON e.group_id = g.id, training t '
                   'LEFT JOIN training_class tc ON t.training_class_id = tc.id '
                   'WHERE g.sport_id = sp.id '
                   'AND g.semester_id = current_semester() '
                   'AND t.group_id = g.id '
                   'AND sp.id = %s '
                   'AND t.start >= %s '
                   'AND t.end <= %s '
                   'GROUP BY g.id, t.id, tc.id', (sport_id, start, end))
    rows = cursor.fetchall()
    return list(map(__tuple_to_training_extended, rows))


def get_students_grades(conn, training_id: int) -> List[TrainingGrade]:
    cursor = conn.cursor()
    cursor.execute('SELECT s.id, s.first_name, s.last_name, s.email, a.hours '
                   'FROM training t, student s, attendance a '
                   'WHERE a.student_id = s.id '
                   'AND a.training_id = %s '
                   'AND s.is_ill = FALSE '
                   'AND t.id = %s '
                   'UNION DISTINCT '
                   'SELECT s.id, s.first_name, s.last_name, s.email, a.hours '
                   'FROM training t, enroll e, student s '
                   'LEFT JOIN attendance a ON a.student_id = s.id AND a.training_id = %s '
                   'WHERE s.id = e.student_id '
                   'AND s.is_ill = FALSE '
                   'AND t.id = %s '
                   'AND t.group_id = e.group_id ', (training_id, training_id, training_id, training_id))
    rows = cursor.fetchall()
    return list(map(__tuple_to_training_grade, rows))
