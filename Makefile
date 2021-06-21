.PHONY: docs

setup:
	poetry install

test:
	poetry run pytest

lint:
	poetry run black classyconf/ tests/

checklint:
	poetry run black --check classyconf/ tests/

docs:
	poetry run make -C docs/ html

clean:
	-find . -iname "*.py[ocd]" -delete
	-find . -iname "__pycache__" -exec rm -rf {} \;
	-rm -rf dist

release: clean lint test docs
	poetry run tbump $(version)

publish:
	poetry publish --build
