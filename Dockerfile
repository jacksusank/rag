FROM pgvector/pgvector:pg16

# Path: Dockerfile
COPY . /app
WORKDIR /app

# setup tables
RUN psql -U postgres -c "CREATE DATABASE totem;"
RUN psql -U postgres -d totem -f /app/sql/schema.sql