import psycopg2
import os

HOST = os.getenv("DATABASE_HOST")
DATABASE = os.getenv("DATABASE_NAME")
USER = os.getenv("DATABASE_USER")
PASSWORD = os.getenv("DATABASE_PASSWORD")

def connect(host=HOST, port=None, database=DATABASE, user=USER, password=PASSWORD):
    try:
        connection = psycopg2.connect(
            host=host,
            port=port if port else None,
            database=database,
            user=user,
            password=password
        )
        return connection
    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL database: {e}")
        return None