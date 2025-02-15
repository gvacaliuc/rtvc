from pydantic import BaseModel

from app.models.contact import Contact
from app.models.call import VoiceCallConfiguration


class CallRequest(BaseModel):
    contact: Contact
    configuration: VoiceCallConfiguration


class CallResponse(BaseModel):
    twilio_call_sid: str
