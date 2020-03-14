import os
import psycopg2

POSTGRES_USER = os.environ['POSTGRES_USER']
POSTGRES_PASSWORD = os.environ['POSTGRES_PASSWORD']
POSTGRES_DB = os.environ['POSTGRES_DB']


def create_connection():
    try:
        connection = psycopg2.connect(
            host='127.0.0.1',
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD)
        return connection
    except psycopg2.DatabaseError as e:
        print("Connection to database failed", e)
        exit(1)


conn = create_connection()
