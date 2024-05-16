psql -h localhost -U postgres -p 5432 -c "CREATE DATABASE totem;"
psql -h localhost -U postgres -p 5432 -d totem -c "CREATE EXTENSION vector;"
psql -h localhost -U postgres -p 5432 -d totem -f ./sql/schema.sql