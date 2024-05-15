# rag

Repo for all work relating to my Totem Rag RFP project.



docker build -t totem_image .
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=test totem_image

docker logs <container_id>