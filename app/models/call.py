from __future__ import annotations

from enum import Enum
from typing import Annotated, Dict, Any, Union, Literal, Final
from pydantic import AfterValidator, BaseModel, Field, validator
from jsonschema import Draft7Validator, SchemaError


class CallIntent(BaseModel):
    description: str = Field(
        ..., description="A brief description of the call's purpose."
    )
    goal: str = Field(
        ..., description="Detailed explanation of what the call aims to achieve."
    )


class TurnTaking(BaseModel):
    value: Union[Wait, SpeakFirst] = Field(discriminator="type")

    class Wait(BaseModel):
        type: Literal["wait"]

    class SpeakFirst(BaseModel):
        type: Final[Literal["speak_first"]]
        initial_delay: float = Field(
            1.0, description="Delay in seconds before the model speaks"
        )


def _validate_jsonschema(schema: str) -> str:
    try:
        Draft7Validator.check_schema(schema)
    except SchemaError as e:
        raise ValueError(f"Invalid JSON Schema: {e}")
    return schema


class VoiceCallConfiguration(BaseModel):
    intent: CallIntent = Field(..., description="Intent parameters for the voice call.")
    turn_taking: Annotated[
        TurnTaking, Field(description="Turn-taking parameters for the conversation.")
    ]
    output_schema: Annotated[
        str,
        AfterValidator(_validate_jsonschema),
        Field(
            description="A JSONSchema document describing the expected output structure of the call."
        ),
    ]


# Example usage:

# Using the 'speak_first' variant:
speak_first_config = VoiceCallConfiguration(
    intent=CallIntent(
        description="Customer support call regarding a billing issue.",
        goal="Resolve the billing dispute by clarifying charges and offering adjustments.",
    ),
    turn_taking=SpeakFirstTurn(initial_delay=1.5),
    output_schema={
        "type": "object",
        "properties": {
            "invoice_number": {
                "type": "string",
                "description": "Invoice number extracted from the call.",
            },
            "disputed_amount": {"type": "number", "description": "Amount in dispute."},
            "resolution": {
                "type": "string",
                "description": "Resolution details, e.g., 'pending', 'approved', etc.",
            },
        },
        "required": ["invoice_number", "disputed_amount", "resolution"],
        "additionalProperties": False,
    },
)

# Using the 'wait' variant:
wait_config = VoiceCallConfiguration(
    intent=CallIntent(
        description="Follow-up call for additional customer details.",
        goal="Collect more detailed account information.",
    ),
    turn_taking=WaitTurn(),
    output_schema={
        "type": "object",
        "properties": {
            "account_id": {
                "type": "string",
                "description": "The customer's account identifier.",
            },
            "update_status": {
                "type": "string",
                "description": "Status of the update, e.g., 'received', 'pending', etc.",
            },
        },
        "required": ["account_id", "update_status"],
        "additionalProperties": False,
    },
)

if __name__ == "__main__":
    # Print the configurations to verify correctness.
    print("Speak First Config:")
    print(speak_first_config.json(indent=2))
    print("\nWait Config:")
    print(wait_config.json(indent=2))
