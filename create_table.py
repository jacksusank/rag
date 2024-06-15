# This sccript creates a totemembeddings table in the postgresql totem database

import connect_to_db

try:
    connection = connect_to_db.delete_database()
    connection = connect_to_db.connect()

    print("Connected to the database!")
    # Create a cursor
    cursor = connection.cursor()

    make_table_query = """
    CREATE VIRTUAL TABLE IF NOT EXISTS embeddings USING vec0(embedding float[768]);"""

    make_data_table_query = """
    CREATE TABLE data (
        id INTEGER PRIMARY KEY,
        metadata TEXT,
        page_contents TEXT,
        embedding_id INTEGER 
    ) STRICT;"""

    cursor.execute(make_table_query)
    cursor.execute(make_data_table_query)
    print("Table created successfully!")
    connection.commit()

    # Close cursor and connection
    cursor.close()
    connection.close()
except Exception as e:
    print("An error occurred:", e)
