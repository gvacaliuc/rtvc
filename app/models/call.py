from __future__ import annotations

from typing import Annotated, Union, Literal
from pydantic import AfterValidator, BaseModel, Field
from referencing.jsonschema import Schema as JSONSchema
from .validators import validate_jsonschema

"""
StartCallRequest:
  intent
  behavior
    personality
    turn taking
  output
"""


class CallIntent(BaseModel):
    description: Annotated[
        str, Field(description="A description of the call's purpose.")
    ]
    goal: Annotated[
        str,
        Field(description="A detailed explanation of what the call aims to achieve."),
    ]


class Personality(BaseModel):
    system_message: Annotated[
        str, Field(description="Raw system message provided to the audio model.")
    ]
    voice: Annotated[
        str, Field(default="allow", description="The voice used by the audio model.")
    ] = "alloy"
    temperature: float = Field(
        default=0.8,
        description="High values will result in higher variance responses, lower values will result in more predictability",
    )


class Behavior(BaseModel):
    personality: Personality
    turn_taking: Union[Wait, SpeakFirst] = Field(discriminator="type")

    class Wait(BaseModel):
        type: Literal["wait"] = "wait"

    class SpeakFirst(BaseModel):
        type: Literal["speak_first"] = "speak_first"
        _DEFAULT_INITIAL_DELAY = 1.0
        initial_delay: float = Field(
            default=_DEFAULT_INITIAL_DELAY,
            description="Delay in seconds before the model speaks",
        )
        initial_message: str


class VoiceCallConfiguration(BaseModel):
    intent: Annotated[
        CallIntent, Field(description="Intent parameters for the voice call.")
    ]
    behavior: Annotated[
        Behavior,
        Field(
            description="Controls behavior of the audio model, such as when conversation is initiated."
        ),
    ]
    output_schema: Annotated[
        JSONSchema,
        AfterValidator(validate_jsonschema),
        Field(
            description="A JSONSchema document describing the expected output structure of the call."
        ),
    ]
