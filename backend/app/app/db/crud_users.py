from typing import List, Tuple


def create_user(conn, first_name: str, last_name: str, email: str, user_type: int, course_id: str = None):
    """
    Creates new user of any type
    @param conn - Database connection
    @param first_name: str - first name of created user
    @param last_name: str - last name of created user
    @param email: str - email of created user, should be unique
    @param user_type: str - type of created user,
        type 0 = student
        type 1 = trainer
        type 2 = student + trainer
        type 3 = admin
    @param course_id: str - course identifier, needed only for students, e. g. 'B18'
    """
    cursor = conn.cursor()
    cursor.execute('INSERT INTO "user" (first_name, last_name, email, type, course_id) VALUES (%s, %s, %s, %s, %s)',
                   (first_name, last_name, email, user_type, course_id))
    conn.commit()


def get_students(conn, course_id: str = None) -> List[Tuple[int, str, str, str, str]]:
    """
    Retrieves registered students
    @param conn - Database connection
    @param course_id: str - particular course identifier, leave empty for choosing all courses
    @return list of tuples (user_id, first_name, last_name, email, course_id)
    """
    cursor = conn.cursor()
    if course_id is None:
        cursor.execute('SELECT id, first_name, last_name, email, course_id FROM "user" WHERE type=0 OR type=2')
    else:
        cursor.execute(
            'SELECT id, first_name, last_name, email, course_id FROM "user" WHERE (type=0 OR type=2) AND course_id=%s',
            (course_id,))
    return cursor.fetchall()


def get_trainers(conn) -> List[Tuple[int, str, str, str]]:
    """
    Retrieves registered trainers / club-leaders
    @param conn - Database connection
    @return list of tuples (user_id, first_name, last_name, email)
    """
    cursor = conn.cursor()
    cursor.execute('SELECT id, first_name, last_name, email FROM "user" WHERE type=1 OR type=2')
    return cursor.fetchall()


def get_user(conn, user_id: int) -> Tuple[int, str, str, str, str]:
    """
    Retrieves registered user by its id
    @param conn - Database connection
    @param user_id: int - searched user id
    @return user tuple (user_id, first_name, last_name, email, course_id)
    """
    cursor = conn.cursor()
    cursor.execute('SELECT id, first_name, last_name, email, course_id FROM "user" WHERE id=%s', (user_id,))
    return cursor.fetchone()


def find_user_by_email(conn, email: str) -> Tuple[int, str, str, str, str]:
    """
    Finds registered user by its email
    @param conn - Database connection
    @param email: str - searched user email
    @return user tuple (user_id, first_name, last_name, email, course_id)
    """
    cursor = conn.cursor()
    cursor.execute('SELECT id, first_name, last_name, email, course_id FROM "user" WHERE email=%s', (email,))
    return cursor.fetchone()
