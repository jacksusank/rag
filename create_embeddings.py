# This script adds the embeddings to the totemembeddings table in the totem database.
import json

# from psycopg2.extras import execute_values
from sentence_transformers import SentenceTransformer

from connect_to_db import connect, serialize_f32
from XMLScanner import read_file


def main():
    documents = read_file()
    page_contents_list = [doc["page_content"] for doc in documents]
    metadata = [json.dumps(doc["metadata"]) for doc in documents]

    model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
    # pool = model.start_multi_process_pool(["cpu", "cpu"])
    # embeddings = model.encode_multi_process(
    #     page_contents_list, pool=pool, chunk_size=50
    # )
    # model.stop_multi_process_pool(pool)
    embeddings = model.encode(
        page_contents_list,
        show_progress_bar=True,
        normalize_embeddings=True,
        batch_size=64,
    )
    # Generic version
    # connection = psycopg2.connect(
    #     host="localhost", port="5432", database="totem", user="postgres", password="test"
    # )
    connection = connect()

    # Create a cursor
    cursor = connection.cursor()

    formatted_embeddings = [
        (i, serialize_f32(embedding.tolist())) for i, embedding in enumerate(embeddings)
    ]

    insert_sql = """
    INSERT INTO embeddings(rowid, embedding) VALUES (?, ?)
    """

    cursor.executemany(insert_sql, formatted_embeddings)

    # Iterate over formatted embeddings, page_content, and metadata and insert them into the database

    items = zip(range(len(page_contents_list)), page_contents_list, metadata)
    # for embedding, page_contents, meta in zip(
    #     formatted_embeddings, page_contents_list, metadata
    # ):
    # items.append([embedding, page_contents, json.dumps(meta)])
    # items.append([page_contents, json.dumps(meta)])

    # # Construct the INSERT query
    # insert_query = """
    # INSERT INTO totemembeddings (embeddings, page_contents, metadata)
    # VALUES (%s, %s, %s)
    # ON CONFLICT (metadata) DO NOTHING;
    # """
    # # Execute the INSERT query
    # cursor.execute(insert_query, (embedding, page_contents, json.dumps(meta)))

    insert_sql = """
    INSERT INTO data (embedding_id, page_contents, metadata)
    VALUES(?, ?, ?)
    """

    # this is optional
    # value_template = "(%s, %s, %s)"
    cursor.executemany(insert_sql, items)
    # execute_values(cursor, insert_sql, items, value_template)
    # Commit the transaction
    connection.commit()

    # Close cursor and connection
    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()
