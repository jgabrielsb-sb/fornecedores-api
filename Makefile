.PHONY: clean

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.py[co]" -delete
	find . -type f -name "*~" -delete


test-unit:
	uv run pytest -m unit

test-e2e:
	APP_ENV=test uv run pytest -m e2e

###### DATABASE MANAGEMENT COMMANDS ######
db-insert-initial-data:
	python src/fornecedores_app/db/scripts/insert_initial_data.py


