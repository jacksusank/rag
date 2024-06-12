# This script adds the embeddings to the totemembeddings table in the totem database.
import json

import psycopg2
from psycopg2.extras import execute_values
from sentence_transformers import SentenceTransformer
from connect_to_db import connect

from XMLScanner import documents

documents_length = documents.__len__()
page_contents_list = [doc["page_content"] for doc in documents]
metadata = [doc["metadata"] for doc in documents]

model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
embeddings = model.encode(page_contents_list, show_progress_bar=True)

# Generic version
# connection = psycopg2.connect(
#     host="localhost", port="5432", database="totem", user="postgres", password="test"
# )
connection = connect()

# Create a cursor
cursor = connection.cursor()

formatted_embeddings = [embedding.tolist() for embedding in embeddings]

# Iterate over formatted embeddings, page_content, and metadata and insert them into the database
items = []

for embedding, page_contents, meta in zip(formatted_embeddings, page_contents_list, metadata):
    items.append([embedding, page_contents, json.dumps(meta)])

    
    # # Construct the INSERT query
    # insert_query = """
    # INSERT INTO totemembeddings (embeddings, page_contents, metadata)
    # VALUES (%s, %s, %s)
    # ON CONFLICT (metadata) DO NOTHING;
    # """
    # # Execute the INSERT query
    # cursor.execute(insert_query, (embedding, page_contents, json.dumps(meta)))

insert_sql = """
INSERT INTO totemembeddings (embeddings, page_contents, metadata)
VALUES %s
ON CONFLICT (metadata) DO NOTHING;
"""

# this is optional
value_template="(%s, %s, %s)"



execute_values(cursor, insert_sql, items, value_template)
# Commit the transaction
connection.commit()

# Close cursor and connection
cursor.close()
connection.close()
