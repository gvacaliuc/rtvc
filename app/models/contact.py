from typing import Annotated, Literal
from pydantic import BaseModel, Field


class ContactID(BaseModel):
    type: Literal["id"]
    id: str


# TODO: add better validation
class PhoneNumber(BaseModel):
    type: Literal["phone_number"]
    number: Annotated[str, Field(pattern="[0-9]{10}")]


Contact = Annotated[ContactID | PhoneNumber, Field(discriminator="type")]
