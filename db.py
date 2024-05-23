def get_db(db_name="totem"):
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database=db_name,
        user="postgres",
        password="test",
    )
    return connection


def db_exists(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT 1 FROM pg_database WHERE datname='totem'")
    return cursor.fetchone() is not None
