up:
	cat .env | xargs -J % env % .venv/bin/fastapi dev app/main.py

shell:
	uv run ipython

set-secrets:
	cat .env | tr -d "'" | fly secrets import

.PHONY: up set-secrets shell
