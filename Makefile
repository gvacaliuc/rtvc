up:
	cat .env | xargs -J % env % .venv/bin/fastapi dev app/main.py

.venv: uv.lock
	uv venv

shell:
	uv run ipython

test:
	uv run pytest

set-secrets:
	cat .env | tr -d "'" | fly secrets import

.PHONY: up set-secrets shell
