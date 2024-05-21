install: .venv
	pip install -r requirements.txt

run_db:
	docker run -it -p 5432:5432 -e POSTGRES_PASSWORD=test pgvector/pgvector:pg16

create_table:
	python create_table.py

clear_table:
	python clear_table.py

delete_table:
	python delete_table.py

embeddings:
	python create_embeddings.py 

# Run like: QUERY="query" make search
search:
	python search.py "${QUERY}"

.venv:
	python3 -m venv .venv