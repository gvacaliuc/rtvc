from fastapi import FastAPI

from app import pydantic64
from app.gateway.twilio import TwilioGateway, MakeCallRequest
from app.models.contact import PhoneNumber
from .models import CallRequest, CallResponse

calls = FastAPI()


@calls.post("/start")
async def start_call_handler(request: CallRequest) -> CallResponse:
    if not isinstance(request.contact, PhoneNumber):
        raise NotImplementedError("calling by contact ID")

    gtw = TwilioGateway.instance()

    request_b64 = pydantic64.encode(request.configuration)
    response = await gtw.make_call(
        MakeCallRequest(
            phone_number=request.contact,
            request_b64=request_b64,
        )
    )

    return CallResponse(twilio_call_sid=response.twilio_sid)
