up:
	cat .env | xargs -J % env % .venv/bin/fastapi dev app/main.py

set-secrets:
	cat .env | tr -d "'" | fly secrets import

.PHONY: up set-secrets
