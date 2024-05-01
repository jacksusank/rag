run:
	python NoMoreLangchain.py

xml_to_db:
	python xml_to_db.py

create_embeddings:
	python create_embeddings.py

search:
	python search.py "${QUERY}"

install: .venv
	pip install -r requirements.txt

.venv:
	python3 -m venv .venv