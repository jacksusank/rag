create_embeddings:
	python create_embeddings.py Grants.....xml

# Run like: QUERY="query" make search
search:
	python search.py "${QUERY}"

install: .venv
	pip install -r requirements.txt

create_tables:
	python create_tables.py

run_db:
	docker run -it -p 5432:5432 -e POSTGRES_PASSWORD=test pgvector/pgvector:pg16

.venv:
	python3 -m venv .venv