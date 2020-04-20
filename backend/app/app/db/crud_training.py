from datetime import datetime
from typing import List, Tuple

from ..models.training import Training, TrainingGrade, TrainingInfo


def __tuple_to_training(row: Tuple[int, datetime, datetime, str]) -> Training:
    id, start, end, group_name = row
    return Training(
        id=id,
        start=start,
        end=end,
        group_name=group_name
    )


def __tuple_to_training_for_trainer(row: Tuple[int, datetime, datetime, str]) -> Training:
    id, start, end, group_name = row
    return Training(
        id=id,
        start=start,
        end=end,
        group_name=group_name,
        can_grade=True
    )


def __tuple_to_training_info(row: Tuple[str, datetime, int]) -> TrainingInfo:
    group_name, start, trainer_id = row
    return TrainingInfo(
        group_name=group_name,
        start=start,
        trainer_id=trainer_id
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
    cursor.execute('SELECT g.name, t.start, g.trainer_id '
                   'FROM training t, "group" g '
                   'WHERE t.group_id = g.id AND t.id = %s', (training_id,))
    return __tuple_to_training_info(cursor.fetchone())


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
    cursor.execute('SELECT t.id, t.start, t."end", g.name '
                   'FROM training t, enroll e, "group" g '
                   'WHERE t.start > %s AND t."end" < %s '
                   'AND t.group_id = g.id '
                   'AND e.group_id = g.id '
                   'AND e.student_id = %s '
                   'AND g.semester_id = current_semester()', (start, end, student_id))
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
    cursor.execute('SELECT t.id, t.start, t."end", g.name '
                   'FROM training t, "group" g '
                   'WHERE t.start > %s AND t."end" < %s '
                   'AND t.group_id = g.id '
                   'AND g.trainer_id = %s '
                   'AND g.semester_id = current_semester()', (start, end, trainer_id))
    rows = cursor.fetchall()
    return list(map(__tuple_to_training_for_trainer, rows))


def get_trainings_in_time(conn, sport_id: int, start: datetime, end: datetime) \
        -> List[Tuple[str, datetime, datetime, int, int]]:
    cursor = conn.cursor()
    cursor.execute('SELECT g.name, t.start, t."end", g.capacity, g.id '
                   'FROM sport sp '
                   'JOIN "group" g ON g.sport_id = sp.id AND g.semester_id = current_semester() '
                   'JOIN training t ON t.group_id = g.id '
                   'AND sp.id = %s '
                   'AND t.start >= %s '
                   'AND t.end <= %s', (sport_id, start, end))
    rows = cursor.fetchall()
    return rows


def get_students_grades(conn, training_id: int) -> List[TrainingGrade]:
    cursor = conn.cursor()
    cursor.execute('SELECT s.id, s.first_name, s.last_name, s.email, a.hours '
                   'FROM "group" g, training t, enroll e, student s '
                   'LEFT JOIN attendance a ON a.student_id = s.id AND a.training_id = %s '
                   'WHERE s.id = e.student_id '
                   'AND s.is_ill = FALSE '
                   'AND t.id = %s '
                   'AND t.group_id = g.id '
                   'AND g.id = e.group_id ', (training_id, training_id))
    rows = cursor.fetchall()
    return list(map(__tuple_to_training_grade, rows))
