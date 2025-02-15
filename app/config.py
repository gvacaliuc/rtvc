from typing import Dict
import json
import os


def _must_getenv(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"missing required environment variable '{name}'")
    return value


# Configuration
TWILIO_ACCOUNT_SID = _must_getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = _must_getenv("TWILIO_AUTH_TOKEN")
PHONE_NUMBER_FROM = _must_getenv("PHONE_NUMBER_FROM")
OPENAI_API_KEY = _must_getenv("OPENAI_API_KEY")
DOMAIN = _must_getenv("DOMAIN")

# Read user database from environment variable
AUTHN_DATABASE = _must_getenv("AUTHN_DATABASE")

try:
    users_db: Dict[str, str] = json.loads(AUTHN_DATABASE)
except json.JSONDecodeError:
    raise ValueError("AUTHN_DATABASE must be valid JSON.")

RTVC_TWILIO_USER_USERNAME = _must_getenv("RTVC_TWILIO_USER_USERNAME")
RTVC_TWILIO_USER_PASSWORD = _must_getenv("RTVC_TWILIO_USER_PASSWORD")
