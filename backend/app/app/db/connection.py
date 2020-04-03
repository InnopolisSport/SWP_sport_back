import psycopg2
from app.core.config import *


def create_connection():
    try:
        connection = psycopg2.connect(
            host=POSTGRES_SERVER,
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD)
        return connection
    except psycopg2.DatabaseError as e:
        print("Connection to database failed", e)
        exit(1)
