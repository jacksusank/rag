# This sccript creates a totemembeddings table in the postgresql totem database
import psycopg2

try:
    # Connect to the default "postgres" database
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="postgres",
        user="postgres",
        password="test"
    )

    # Create a cursor
    cursor = connection.cursor()

    # Check if the "totem" database exists
    cursor.execute("SELECT 1 FROM pg_database WHERE datname='totem'")

    # If it doesn't exist, create it
    if cursor.fetchone() is None:
        cursor.execute("COMMIT")
        cursor.execute("CREATE DATABASE totem")

    # Close cursor and connection
    cursor.close()
    connection.close()

    # Generic version
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        database="totem",
        user="postgres",
        password="test"
        )

    print("Connected to the database!")
    # Create a cursor
    cursor = connection.cursor()

    add_extension_query = "CREATE EXTENSION IF NOT EXISTS vector;"  
    cursor.execute(add_extension_query)

    # Create the table if it doesn't exist
    make_table_query = """
    CREATE TABLE IF NOT EXISTS totemembeddings (
        id SERIAL PRIMARY KEY,
        metadata JSONB UNIQUE,
        page_contents TEXT,
        embeddings VECTOR);"""

    cursor.execute(make_table_query)
    print("Table created successfully!") 
    connection.commit()

    # Close cursor and connection
    cursor.close()
    connection.close()
except Exception as e:
    print("An error occurred:", e)