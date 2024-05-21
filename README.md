# rag

Repo for all work relating to my Totem Rag RFP project.

Initial setup:
`make install`
`make run_db`
In another terminal:
`make create_table`

Create embeddings:
`make embeddings`

Query database:
`QUERY="query" make search`

cd /tmp
git clone --branch v0.7.0 https://github.com/pgvector/pgvector.git
cd pgvector
make
make install # may need sudo
