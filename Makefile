up:
	cat .env | xargs -J % env % .venv/bin/fastapi dev app/main.py

.venv: uv.lock
	uv venv

shell:
	uv run ipython

test:
	uv run pytest

lint:
	uv run ruff format --check
	uv run ruff check --fix

set-secrets:
	cat .env | tr -d "'" | fly secrets import

.PHONY: up set-secrets shell
