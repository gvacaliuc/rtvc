from fastapi import WebSocket, HTTPException
from twilio.rest import Client
from twilio.request_validator import RequestValidator

# TODO: maybe make as parameter
from ..config import DOMAIN, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, PHONE_NUMBER_FROM

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

media_stream_url = f"wss://{DOMAIN}/ws/media-stream"

# NOTE:
# * code below initiates outbound call with twilio from an API request

async def check_number_allowed(to: str) -> bool:
    """Check if a number is allowed to be called."""
    try:
        # Uncomment these lines to test numbers. Only add numbers you have permission to call
        # OVERRIDE_NUMBERS = ['+18005551212'] 
        # if to in OVERRIDE_NUMBERS:             
          # return True

        incoming_numbers = client.incoming_phone_numbers.list(phone_number=to)
        if incoming_numbers:
            return True

        outgoing_caller_ids = client.outgoing_caller_ids.list(phone_number=to)
        if outgoing_caller_ids:
            return True

        return False
    except Exception as e:
        print(f"Error checking phone number: {e}")
        return False

async def make_call(phone_number_to_call: str) -> str:
    """Make an outbound call."""
    if not phone_number_to_call:
        raise ValueError("Please provide a phone number to call.")

    is_allowed = await check_number_allowed(phone_number_to_call)
    if not is_allowed:
        raise ValueError(f"The number {phone_number_to_call} is not recognized as a valid outgoing number or caller ID.")

    # Ensure compliance with applicable laws and regulations
    # All of the rules of TCPA apply even if a call is made by AI.
    # Do your own diligence for compliance.

    # TODO: url needs to match domain + router path, move this stuff over there
    outbound_twiml = (
        f'<?xml version="1.0" encoding="UTF-8"?>'
        f'<Response><Connect><Stream url="{media_stream_url}" /></Connect></Response>'
    )

    call = client.calls.create(
        from_=PHONE_NUMBER_FROM,
        to=phone_number_to_call,
        twiml=outbound_twiml
    )

    assert call.sid is not None, "invalid call SID"

    return call.sid


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
        raise HTTPException(status_code=_HTTP_BAD_REQUEST, detail="Missing Twilio signature.")

    if not _request_validator.validate(url, params, twilio_signature):
        await websocket.close(code=_WEBSOCKET_POLICY_VIOLATION)
        raise HTTPException(status_code=_HTTP_FORBIDDEN, detail="Invalid Twilio signature.")
