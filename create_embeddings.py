# This script adds the embeddings to the totemembeddings table in the totem database.
from sentence_transformers import SentenceTransformer
import psycopg2
import json

from XMLScanner import documents
documents_length = documents.__len__()
page_contents_list = [doc['page_content'] for doc in documents]
metadata = [doc['metadata'] for doc in documents]

model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
embeddings = model.encode(page_contents_list, show_progress_bar=True)

# Print embeddings individually
for i, embedding in enumerate(embeddings):
    print(f"Embedding for sentence {i+1}:")
    print(embedding)

# Generic version
connection = psycopg2.connect(
    host="localhost",
    port="5432",
    database="totem",
    user="postgres",
    password="test"
)

# Create a cursor
cursor = connection.cursor()

formatted_embeddings = [embedding.tolist() for embedding in embeddings]


# print(formatted_embeddings[1])
i = 0
# Iterate over formatted embeddings, page_content, and metadata and insert them into the database
for embedding, page_contents, meta in zip(formatted_embeddings, page_contents_list, metadata):
    if i % 50 == 0:
        percent = i / documents_length * 100
        print(percent, " percent done!")
    # Construct the INSERT query
    insert_query = """
    INSERT INTO totemembeddings (embeddings, page_contents, metadata)
    VALUES (%s, %s, %s)
    ON CONFLICT (metadata) DO NOTHING;
    """
    # Execute the INSERT query
    cursor.execute(insert_query, (embedding, page_contents, json.dumps(meta)))
    # Commit the transaction
    # connection.commit()
print("100 percent done!")

# Commit the transaction
connection.commit()

# Close cursor and connection
cursor.close()
connection.close()