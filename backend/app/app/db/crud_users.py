from typing import List, Tuple

from ..models.user import Student, Trainer, Admin


def create_student(conn, first_name: str, last_name: str, email: str):
    """
    Creates new student
    @param conn - Database connection
    @param first_name: str - first name of created user
    @param last_name: str - last name of created user
    @param email: str - email of created user, should be unique
    """
    cursor = conn.cursor()
    cursor.execute('INSERT INTO student (first_name, last_name, email, is_ill) VALUES (%s, %s, %s, FALSE)',
                   (first_name, last_name, email))
    conn.commit()


def create_trainer(conn, first_name: str, last_name: str, email: str):
    """
    Creates new student
    @param conn - Database connection
    @param first_name: str - first name of created user
    @param last_name: str - last name of created user
    @param email: str - email of created user, should be unique
    """
    cursor = conn.cursor()
    cursor.execute('INSERT INTO trainer (first_name, last_name, email) VALUES (%s, %s, %s)',
                   (first_name, last_name, email))
    conn.commit()


def create_admin(conn, first_name: str, last_name: str, email: str):
    """
    Creates new student
    @param conn - Database connection
    @param first_name: str - first name of created user
    @param last_name: str - last name of created user
    @param email: str - email of created user, should be unique
    """
    cursor = conn.cursor()
    cursor.execute('INSERT INTO admin (first_name, last_name, email) VALUES (%s, %s, %s)',
                   (first_name, last_name, email))
    conn.commit()


def __tuple_to_student(row: Tuple[int, str, str, str, bool]) -> Student:
    id, first_name, last_name, email, is_ill = row
    return Student(id=id, first_name=first_name, last_name=last_name, email=email, is_ill=is_ill)


def __tuple_to_trainer(row: Tuple[int, str, str, str]) -> Trainer:
    id, first_name, last_name, email = row
    return Trainer(id=id, first_name=first_name, last_name=last_name, email=email)


def __tuple_to_admin(row: Tuple[int, str, str, str]) -> Admin:
    id, first_name, last_name, email = row
    return Admin(id=id, first_name=first_name, last_name=last_name, email=email)


def get_students(conn) -> List[Student]:
    """
    Retrieves registered students
    @param conn - Database connection
    @return list of all students
    """
    cursor = conn.cursor()
    cursor.execute('SELECT id, first_name, last_name, email, is_ill FROM student')
    return list(map(__tuple_to_student, cursor.fetchall()))


def get_trainers(conn) -> List[Trainer]:
    """
    Retrieves registered trainers
    @param conn - Database connection
    @return list of all trainers
    """
    cursor = conn.cursor()
    cursor.execute('SELECT id, first_name, last_name, email FROM trainer')
    return list(map(__tuple_to_trainer, cursor.fetchall()))


def get_admins(conn) -> List[Admin]:
    """
    Retrieves registered administrators
    @param conn - Database connection
    @return list of all administrators
    """
    cursor = conn.cursor()
    cursor.execute('SELECT id, first_name, last_name, email FROM admin')
    return list(map(__tuple_to_admin, cursor.fetchall()))


def get_student(conn, student_id: int) -> Student:
    """
    Retrieves registered student by its id
    @param conn - Database connection
    @param student_id: int - searched student id
    """
    cursor = conn.cursor()
    cursor.execute('SELECT id, first_name, last_name, email, is_ill FROM student WHERE id=%s',
                   (student_id,))
    row = cursor.fetchone()
    return __tuple_to_student(row) if row is not None else None


def get_trainer(conn, trainer_id: int) -> Trainer:
    """
    Retrieves registered trainer by its id
    @param conn - Database connection
    @param trainer_id: int - searched trainer id
    """
    cursor = conn.cursor()
    cursor.execute('SELECT id, first_name, last_name, email FROM trainer WHERE id=%s',
                   (trainer_id,))
    row = cursor.fetchone()
    return __tuple_to_trainer(row) if row is not None else None


def get_admin(conn, admin_id: int) -> Admin:
    """
    Retrieves registered admin by its id
    @param conn - Database connection
    @param admin_id: int - searched admin id
    """
    cursor = conn.cursor()
    cursor.execute('SELECT id, first_name, last_name, email FROM admin WHERE id=%s',
                   (admin_id,))
    row = cursor.fetchone()
    return __tuple_to_admin(row) if row is not None else None


def find_student(conn, email: str) -> Student:
    """
    Retrieves registered student by its id
    @param conn - Database connection
    @param email: str - searched student email
    """
    cursor = conn.cursor()
    cursor.execute('SELECT id, first_name, last_name, email, is_ill FROM student WHERE email=%s',
                   (email,))
    row = cursor.fetchone()
    return __tuple_to_student(row) if row is not None else None


def find_trainer(conn, email: str) -> Trainer:
    """
    Retrieves registered trainer by its id
    @param conn - Database connection
    @param email: str - searched trainer email
    """
    cursor = conn.cursor()
    cursor.execute('SELECT id, first_name, last_name, email FROM trainer WHERE email=%s',
                   (email,))
    row = cursor.fetchone()
    return __tuple_to_trainer(row) if row is not None else None


def find_admin(conn, email: str) -> Admin:
    """
    Retrieves registered admin by its id
    @param conn - Database connection
    @param email: str - searched admin email
    """
    cursor = conn.cursor()
    cursor.execute('SELECT id, first_name, last_name, email FROM admin WHERE email=%s',
                   (email,))
    row = cursor.fetchone()
    return __tuple_to_admin(row) if row is not None else None
