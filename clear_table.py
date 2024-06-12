import psycopg2
from connect_to_db import connect

# # Generic version
connection = connect()
# connection = psycopg2.connect(
#     host="localhost",
#     port="5432",
#     database="totem",
#     user="postgres",
#     password="test"
#     )

cursor = connection.cursor()

# Check if the table exists
cursor.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE  table_schema = 'public'
        AND    table_name   = 'totemembeddings'
    )
""")

# If it exists, truncate it
if cursor.fetchone()[0]:
    cursor.execute("TRUNCATE TABLE totemembeddings RESTART IDENTITY")

connection.commit()
cursor.close()
connection.close()

