up:
	cat .env | xargs -J % env % .venv/bin/fastapi dev app/main.py
