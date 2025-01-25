from typing import Dict
import json
import os

def _must_getenv(name: str) -> str:
    value = os.getenv(name)
    if value is None:
        raise RuntimeError(f"missing required environment variable '{name}'")
    return value

# Configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
PHONE_NUMBER_FROM = os.getenv('PHONE_NUMBER_FROM')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
DOMAIN=os.getenv('DOMAIN')

if not (TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN and PHONE_NUMBER_FROM and OPENAI_API_KEY and DOMAIN):
    raise ValueError('Missing Twilio and/or OpenAI environment variables. Please set them in the .env file.')

# Read user database from environment variable
AUTHN_DATABASE = os.getenv("AUTHN_DATABASE")
if not AUTHN_DATABASE:
    raise ValueError("Environment variable AUTHN_DATABASE is required.")

try:
    users_db: Dict[str, str] = json.loads(AUTHN_DATABASE)
except json.JSONDecodeError:
    raise ValueError("AUTHN_DATABASE must be valid JSON.")

RTVC_TWILIO_USER_USERNAME=_must_getenv("RTVC_TWILIO_USER_USERNAME")
RTVC_TWILIO_USER_PASSWORD=_must_getenv("RTVC_TWILIO_USER_PASSWORD")
