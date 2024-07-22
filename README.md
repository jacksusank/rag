# rag

Repo for all work relating to my Totem Rag RFP project.

Initial setup:
`make install`
`make run_db`
In another terminal:
`make create_table`

Create embeddings:
`make embeddings`

To interact via localhost site:
uvicorn fast_api_search:app --reload

To manually query the database:
`QUERY="query" make search`

cd /tmp
git clone --branch v0.7.0 https://github.com/pgvector/pgvector.git
cd pgvector
make
make install # may need sudo
