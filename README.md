# rag

Repo for all work relating to my Totem Rag RFP project.

Initial setup:
`make install`
`make run_db`
`make create_tables`

Create embeddings:
`make embeddings`

Query database:
`QUERY="query" make search`

docker build -t totem_image .
docker run -it -p 5432:5432 -e POSTGRES_PASSWORD=test totem_image


docker logs <container_id>
