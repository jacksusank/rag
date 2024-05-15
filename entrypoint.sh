#!/bin/bash
set -e

# Initialize the database and start the PostgreSQL server process
docker-entrypoint.sh postgres &

# Wait for PostgreSQL to initialize
until psql -U postgres -c '\l'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

# Set up the database
psql -U postgres -c "CREATE DATABASE totem;"
psql -U postgres -d totem -f /app/sql/schema.sql

# Run the Python script
python3 AllMpnetV2.py
python3 NewQueryTool.py