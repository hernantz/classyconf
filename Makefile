setup:
	poetry install

test:
	poetry run pytest

lint:
	poetry run black classyconf/ tests/

checklint:
	poetry run black --check classyconf/ tests/

clean:
	-find . -iname "*.py[ocd]" -delete
	-find . -iname "__pycache__" -exec rm -rf {} \;
	-rm -rf dist

release: clean lint test
	git tag `poetry version --short`
	git push origin `poetry version --short`
	rm -rf dist/*
	poetry publish --build
