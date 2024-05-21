import psycopg2

# Generic connection to the database
connection = psycopg2.connect(
    host="localhost",
    port="5432",
    database="totem",
    user="postgres",
    password="test"
    )

cursor = connection.cursor()

# Check if the table exists
cursor.execute("""
    SELECT EXISTS (
        SELECT FROM information_schema.tables 
        WHERE  table_schema = 'public'
        AND    table_name   = 'totemembeddings'
    )
""")

# If it exists, delete it
if cursor.fetchone()[0]:
    cursor.execute("DROP TABLE totemembeddings")

connection.commit()
cursor.close()
connection.close()
