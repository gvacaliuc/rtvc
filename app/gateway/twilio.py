from __future__ import annotations
from typing import Optional

from fastapi import WebSocket, HTTPException
from pydantic import BaseModel, Field
from twilio.rest import Client
from twilio.request_validator import RequestValidator

# TODO: maybe make as parameter
from ..config import DOMAIN, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, PHONE_NUMBER_FROM
from .. import pydantic64

media_stream_url = f"wss://{DOMAIN}/ws/media-stream"

# * intent
# * system message
# * voice
# * temperature
# * first message


# TODO: add validation
class PhoneNumber(BaseModel):
    number: str = Field(pattern="[0-9]{10}")


class CallIntent(BaseModel):
    system_message: str
    voice: str
    temperature: float
    opening_message: Optional[str]


class MakeCallRequest(BaseModel):
    phone_number: PhoneNumber
    call_intent: CallIntent


class MakeCallResponse(BaseModel):
    twilio_sid: str


class TwilioGateway:
    _instance: Optional[TwilioGateway] = None
    _client: Client

    def __init__(self, client: Client):
        self._client = client

    @classmethod
    def instance(cls) -> TwilioGateway:
        if cls._instance is None:
            cls._instance = TwilioGateway(
                client=Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
            )
        return cls._instance

    async def make_call(self, request: MakeCallRequest) -> MakeCallResponse:
        """
        Initiates an outbound call using the Twilio API.
        """
        number = request.phone_number.number
        is_allowed = await self._check_number_allowed(number)
        if not is_allowed:
            raise ValueError(
                f"The number {number} is not recognized as a valid outgoing number or caller ID."
            )

        # Ensure compliance with applicable laws and regulations
        # All of the rules of TCPA apply even if a call is made by AI.
        # Do your own diligence for compliance.

        request_encoded = pydantic64.encode(request)

        # TODO: url needs to match domain + router path, move this stuff over there
        outbound_twiml = (
            f'<?xml version="1.0" encoding="UTF-8"?>'
            f'<Response><Connect><Stream url="{media_stream_url}"><Parameter name="request" value="{request_encoded}"/></Stream></Connect></Response>'
        )

        call = self._client.calls.create(
            from_=PHONE_NUMBER_FROM, to=number, twiml=outbound_twiml
        )

        assert call.sid is not None, "invalid call SID"

        return MakeCallResponse(twilio_sid=call.sid)

    async def _check_number_allowed(self, to: str) -> bool:
        """Check if a number is allowed to be called."""
        try:
            # Uncomment these lines to test numbers. Only add numbers you have permission to call
            # OVERRIDE_NUMBERS = ['+18005551212']
            # if to in OVERRIDE_NUMBERS:
            # return True

            incoming_numbers = self._client.incoming_phone_numbers.list(phone_number=to)
            if incoming_numbers:
                return True

            outgoing_caller_ids = self._client.outgoing_caller_ids.list(phone_number=to)
            if outgoing_caller_ids:
                return True

            return False
        except Exception as e:
            print(f"Error checking phone number: {e}")
            return False


_WEBSOCKET_POLICY_VIOLATION = 1008
_HTTP_BAD_REQUEST = 400
_HTTP_FORBIDDEN = 403
_request_validator = RequestValidator(TWILIO_AUTH_TOKEN)


async def validate_media_stream(websocket: WebSocket):
    """
    Validates that the websocket was initiated by Twilio.
    """

    headers = websocket.headers

    # NOTE: we don't handle SSL termination within this application (thanks
    # fly!), so the websocket URL reported by fastapi has incorrect protocol.
    url = str(websocket.url).replace("ws://", "wss://")

    # TODO: always empty rn, not sure if we should be using these or just {}
    params = websocket.query_params

    twilio_signature = headers.get("X-Twilio-Signature")

    if not twilio_signature:
        await websocket.close(code=_WEBSOCKET_POLICY_VIOLATION)
        raise HTTPException(
            status_code=_HTTP_BAD_REQUEST, detail="Missing Twilio signature."
        )

    if not _request_validator.validate(url, params, twilio_signature):
        await websocket.close(code=_WEBSOCKET_POLICY_VIOLATION)
        raise HTTPException(
            status_code=_HTTP_FORBIDDEN, detail="Invalid Twilio signature."
        )
