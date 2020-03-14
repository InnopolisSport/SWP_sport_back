from app.db.connection import conn


# type 0 = student
# type 1 = trainer
# type 2 = student + trainer
# type 3 = admin
def create_user(first_name: str, last_name: str, email: str, user_type: int, course_id: str = None):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO "user" (first_name, last_name, email, type, course_id) VALUES (%s, %s, %s, %s, %s)',
                   (first_name, last_name, email, user_type, course_id))
    conn.commit()


def get_students():
    cursor = conn.cursor()
    cursor.execute('SELECT id, first_name, last_name, email, course_id FROM "user" WHERE type=0 OR type=2')
    return cursor.fetchall()


def get_trainers():
    cursor = conn.cursor()
    cursor.execute('SELECT id, first_name, last_name, email FROM "user" WHERE type=1 OR type=2')
    return cursor.fetchall()


def get_user(user_id):
    cursor = conn.cursor()
    cursor.execute('SELECT first_name, last_name, email, course_id FROM "user" WHERE id=%s', (user_id,))
    return cursor.fetchone()


def find_user_by_email(email):
    cursor = conn.cursor()
    cursor.execute('SELECT id, first_name, last_name, email, course_id FROM "user" WHERE email=%s', (email,))
    return cursor.fetchone()
