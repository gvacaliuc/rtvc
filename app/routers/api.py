from fastapi import FastAPI
from pydantic import BaseModel
from starlette.middleware.authentication import AuthenticationMiddleware

from ..authn import BasicAuthBackend
from ..gateway.twilio import make_call

app = FastAPI()
app.add_middleware(AuthenticationMiddleware, backend=BasicAuthBackend(), on_error=BasicAuthBackend.on_auth_error)

class CallRequest(BaseModel):
    number: str

class CallResponse(BaseModel):
    twilio_call_sid: str

@app.post("/call")
async def start_call_handler(request: CallRequest) -> CallResponse:
    sid = await make_call(request.number)
    return CallResponse(twilio_call_sid=sid)
