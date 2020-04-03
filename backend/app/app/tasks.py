from datetime import datetime, date, timedelta

from app.db.connection import create_connection


def get_next_monday() -> date:
    today = date.today()
    return today + timedelta(days=-today.weekday(), weeks=1)


def get_current_monday() -> date:
    today = date.today()
    return today - timedelta(days=today.weekday())


def generate_trainings(group_id: int, monday: date = None):
    conn = create_connection()
    cursor = conn.cursor()
    if monday is None:
        monday = get_next_monday()

    cursor.execute("""SELECT weekday, start, "end" from schedule where group_id=%s""", (group_id,))
    for schedule in cursor.fetchall():
        weekday, start, end = schedule
        training_day = monday + timedelta(days=weekday)

        training_start = datetime.combine(
            date=training_day,
            time=start
        )

        training_end = datetime.combine(
            date=training_day,
            time=end
        )

        cursor.execute("""insert into training (group_id, start, "end") values (%s, %s, %s)""",
                       (group_id, training_start, training_end)
                       )
    conn.commit()
    cursor.close()
    conn.close()

# generate_trainings(1, get_current_monday())
