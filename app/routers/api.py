from fastapi import APIRouter
from pydantic import BaseModel

from ..gateway.twilio import make_call

router = APIRouter()

class CallRequest(BaseModel):
    number: str

class CallResponse(BaseModel):
    twilio_call_sid: str

@router.post("/call")
async def start_call_handler(request: CallRequest) -> CallResponse:
    sid = await make_call(request.number)
    return CallResponse(twilio_call_sid=sid)
