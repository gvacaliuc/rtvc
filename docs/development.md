# development

## prerequisites

* OpenAI account
* twilio account + phone number
* internet accessible domain (either ngrok or deployed VPC, like fly.io) that twilio can access
* the following secrets set in the `.env` file:

### secrets

these need to be set in the local `.env` file

```
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
# your twilio phone number
PHONE_NUMBER_FROM=
OPENAI_API_KEY=
# the public domain that twilio can access
DOMAIN=
# JSON user database, use scripts/add-user.py to add a user
# API routes are authenticated using HTTP Basic against these users
AUTNN_DATABASE=
```
