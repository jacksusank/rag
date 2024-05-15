from sentence_transformers import SentenceTransformer
import psycopg2
import json


from XMLScanner import documents
documents = documents[:10]
page_contents_list = [doc['page_content'] for doc in documents]
metadata = [doc['metadata'] for doc in documents]


model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
embeddings = model.encode(page_contents_list)


# Access embeddings individually
for i, embedding in enumerate(embeddings):
    print(f"Embedding for sentence {i+1}:")
    print(embedding)


# Generic version
connection = psycopg2.connect(
    host="localhost",
    port="5432",
    database="totem",
    user="postgres"
)


# My version of connecting to PostgreSQL
# connection = psycopg2.connect(
#     host="localhost",
#     port="5432",
#     database="vector_db",
#     user="postgres",
#     password="test"
# )

# Create a cursor
cursor = connection.cursor()

# Remove contents in the existing collection (table)
truncate_query = "TRUNCATE TABLE totemembeddings RESTART IDENTITY;"
cursor.execute(truncate_query)
connection.commit()


# Convert embeddings to a suitable format (e.g., list of floats)
# partly_formatted_embeddings = [list(embedding) for embedding in embeddings]
# fully_formatted_embeddings = [list(part[0])[1:][0] for part in partly_formatted_embeddings]
# fully_formatted_embeddings = [list(part[0])[1] for part in partly_formatted_embeddings]

partly_formatted_embeddings = [embedding.tolist() for embedding in embeddings]



# print(fully_formatted_embeddings[1])

# Iterate over fully formatted embeddings, page_content, and metadata and insert them into the database
for embedding, page_contents, meta in zip(partly_formatted_embeddings, page_contents_list, metadata):
    # Construct the INSERT query
    insert_query = """
    INSERT INTO totemembeddings (embeddings, page_contents, metadata)
    VALUES (%s, %s, %s);
    """
    # Execute the INSERT query
    cursor.execute(insert_query, (embedding, page_contents, json.dumps(meta)))
    # Commit the transaction
    connection.commit()

# Close cursor and connection
cursor.close()
connection.close()