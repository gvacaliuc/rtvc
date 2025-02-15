from __future__ import annotations

from typing import Annotated, Union, Literal
from pydantic import AfterValidator, BaseModel, Field
from jsonschema import Draft7Validator, SchemaError
from referencing.jsonschema import Schema as JSONSchema


class CallIntent(BaseModel):
    description: Annotated[
        str, Field(description="A description of the call's purpose.")
    ]
    goal: Annotated[
        str,
        Field(description="A detailed explanation of what the call aims to achieve."),
    ]


class TurnTaking(BaseModel):
    value: Union[Wait, SpeakFirst] = Field(discriminator="type")

    class Wait(BaseModel):
        type: Literal["wait"] = "wait"

    class SpeakFirst(BaseModel):
        type: Literal["speak_first"] = "speak_first"
        _DEFAULT_INITIAL_DELAY = 1.0
        initial_delay: float = Field(
            default=_DEFAULT_INITIAL_DELAY,
            description="Delay in seconds before the model speaks",
        )


def _validate_jsonschema(schema: JSONSchema) -> JSONSchema:
    try:
        Draft7Validator.check_schema(schema)
    except SchemaError as e:
        raise ValueError(f"Invalid JSON Schema: {e}")
    return schema


class VoiceCallConfiguration(BaseModel):
    intent: Annotated[
        CallIntent, Field(description="Intent parameters for the voice call.")
    ]
    turn_taking: Annotated[
        TurnTaking, Field(description="Turn-taking parameters for the conversation.")
    ]
    output_schema: Annotated[
        JSONSchema,
        AfterValidator(_validate_jsonschema),
        Field(
            description="A JSONSchema document describing the expected output structure of the call."
        ),
    ]
