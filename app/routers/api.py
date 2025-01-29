from fastapi import FastAPI
from pydantic import BaseModel, Field
from starlette.middleware.authentication import AuthenticationMiddleware

from ..authn import BasicAuthBackend
from ..gateway.twilio import CallIntent, PhoneNumber, TwilioGateway, MakeCallRequest

app = FastAPI()
app.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend(["admin"]), on_error=BasicAuthBackend.on_auth_error)

class CallRequest(BaseModel):
    number: str = Field(pattern="[0-9]{10}")
    system_message: str

class CallResponse(BaseModel):
    twilio_call_sid: str

@app.post("/call")
async def start_call_handler(request: CallRequest) -> CallResponse:
    gtw = TwilioGateway.instance()

    response = await gtw.make_call(MakeCallRequest(
        phone_number=PhoneNumber(
            number=request.number,
        ),
        call_intent=CallIntent(
            system_message=request.system_message,
            voice="",
            temperature=0.8,
            opening_message="What's up doc?",
        )
    ))

    return CallResponse(twilio_call_sid=response.twilio_sid)
