.PHONY: help install run test lint format clean migrate downgrade

help:
	@echo "Available commands:"
	@echo "  install     Install dependencies"
	@echo "  run        Start development server"
	@echo "  test       Run tests"
	@echo "  lint       Run linters"
	@echo "  format     Format code"
	@echo "  clean      Clean cache files"
	@echo "  migrate    Run database migrations"
	@echo "  downgrade  Rollback last migration"

install:
	pip install -r requirements.txt
	pre-commit install

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -v

lint:
	flake8 .
	mypy .

format:
	black .
	isort .

clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type f -name ".coverage" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} +
	find . -type d -name "*.egg" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +

migrate:
	alembic upgrade head

downgrade:
	alembic downgrade -1
