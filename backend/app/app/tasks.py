from datetime import datetime, date, timedelta
from typing import Optional

from app.db.connection import create_connection


def get_next_monday() -> date:
    today = date.today()
    return today + timedelta(days=-today.weekday(), weeks=1)


def get_current_monday() -> date:
    today = date.today()
    return today - timedelta(days=today.weekday())


def generate_trainings(group_id: Optional[int] = None, monday: date = None, conn=None, cursor=None):
    """
    Generates trainings for a given group (if given group_id) or for all otherwise,
    starting with week of given monday (if given) or next week otherwise
    :param group_id:
    :param monday:
    :param conn:
    :param cursor:
    """
    new = False
    if cursor is None:
        new = True
        conn = create_connection()
        cursor = conn.cursor()
    if monday is None:
        monday = get_next_monday()
    if group_id is None:
        cursor.execute("""SELECT weekday, start, "end", group_id from schedule""")
    else:
        cursor.execute("""SELECT weekday, start, "end", group_id from schedule where group_id=%s""", (group_id,))
    for schedule in cursor.fetchall():
        weekday, start, end, group_id = schedule
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

    if new:
        cursor.close()
        conn.close()


generate_trainings(group_id=None,
                   monday=get_current_monday()
                   )
