from app.db import conn


def create_sport(name: str):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO sport (name) VALUES (%s)', (name,))
    conn.commit()


def delete_sport(sport_id):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM sport WHERE id=%s', (sport_id,))
    conn.commit()


def create_group(name: str, sport_id: int):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO "group" (name, sport_id) VALUES (%s, %s)', (name, sport_id))
    conn.commit()


def get_groups():
    cursor = conn.cursor()
    cursor.execute('SELECT g.id, g.name, s.name FROM "group" g JOIN sport s ON g.sport_id = s.id')
    return cursor.fetchall()


def delete_group(group_id):
    cursor = conn.cursor()
    cursor.execute('DELETE FROM "group" WHERE id=%s', (group_id,))
    conn.commit()
