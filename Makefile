install:
	poetry install

lint:
	poetry run ruff check .

test:
	poetry run pytest -v -s --cov=visarate tests

publish:
	poetry build -f wheel
	poetry publish

.PHONY: lint test publish
