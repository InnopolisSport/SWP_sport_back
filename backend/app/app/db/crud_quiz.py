from app.db.connection import conn


def create_quiz(author_id: int):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO quiz (author_id) VALUES (%s)', (author_id,))
    conn.commit()


def insert_priorities(user_id: int, quiz_id: int, priorities: list):
    cursor = conn.cursor()
    for (group, priority) in priorities:
        cursor.execute('INSERT INTO selected_priority (user_id, quiz_id, group_id, priority) VALUES (%s, %s, %s, %s)',
                       (user_id, quiz_id, group, priority))
    conn.commit()


def check_if_user_have_submission(quiz_id, user_id):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM selected_priority WHERE user_id=%s AND quiz_id=%s LIMIT 1', (user_id, quiz_id))
    return cursor.fetchone() is not None


def delete_submission(quiz_id, user_id):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM selected_priority WHERE user_id=%s AND quiz_id=%s', (user_id, quiz_id))
    conn.commit()
