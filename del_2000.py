import psycopg2
from connect_to_db import connect


connection = connect()

cursor = connection.cursor()

sql_query = """
DELETE FROM totemembeddings
WHERE id IN (
    SELECT id
    FROM totemembeddings
    ORDER BY id DESC
    LIMIT 2000
);
"""

cursor.execute(sql_query)

connection.commit()

cursor.close()

connection.close()

