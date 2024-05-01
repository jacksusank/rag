-- Create table called totemembeddings, with columns id, metadata (jsonb), page_contents (text) and embeddings (vector)

CREATE TABLE totemembeddings (
    id SERIAL PRIMARY KEY,
    metadata JSONB,
    page_contents TEXT,
    embeddings VECTOR
);