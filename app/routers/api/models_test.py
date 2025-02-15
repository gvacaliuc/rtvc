import pytest
from pydantic import ValidationError
from referencing.jsonschema import Schema as JSONSchema

from .models import CallRequest

# Sample valid JSON schema
valid_schema: JSONSchema = {
    "type": "object",
    "properties": {"example": {"type": "string"}},
}

# Valid test cases
valid_cases = [
    {
        "contact": {"type": "id", "id": "12345"},
        "configuration": {
            "intent": {
                "description": "Customer support call",
                "goal": "Resolve user account issues",
            },
            "behavior": {
                "personality": {
                    "system_message": "Be helpful and friendly.",
                    "voice": "alloy",
                    "temperature": 0.7,
                },
                "turn_taking": {
                    "type": "speak_first",
                    "initial_delay": 1.5,
                    "initial_message": "Hello, how can I assist you?",
                },
            },
            "output_schema": valid_schema,
        },
    },
    {
        "contact": {"type": "phone_number", "number": "1234567890"},
        "configuration": {
            "intent": {
                "description": "Reminder call",
                "goal": "Remind patient about appointment",
            },
            "behavior": {
                "personality": {
                    "system_message": "Be professional and concise.",
                    "voice": "nova",
                    "temperature": 0.5,
                },
                "turn_taking": {"type": "wait"},
            },
            "output_schema": valid_schema,
        },
    },
]

# Invalid test cases
invalid_cases = [
    # Missing required fields
    {
        "contact": {"type": "id"},
        "configuration": {
            "intent": {"goal": "Missing description"},
            "behavior": {
                "personality": {"system_message": "Be warm.", "temperature": 0.9},
                "turn_taking": {
                    "type": "speak_first",
                    "initial_message": "Hello there!",
                },
            },
            "output_schema": valid_schema,
        },
    },
    # Invalid phone number
    {
        "contact": {"type": "phone_number", "number": "12345"},
        "configuration": {
            "intent": {"description": "Sales call", "goal": "Introduce new product"},
            "behavior": {
                "personality": {
                    "system_message": "Be engaging.",
                    "voice": "alloy",
                    "temperature": 1.0,
                },
                "turn_taking": {
                    "type": "speak_first",
                    "initial_delay": 2.0,
                    "initial_message": "Hello! Have you heard about our product?",
                },
            },
            "output_schema": valid_schema,
        },
    },
    # Invalid schema (missing discriminator)
    {
        "contact": {"type": "unknown_type", "id": "12345"},
        "configuration": {
            "intent": {"description": "Test call", "goal": "Testing"},
            "behavior": {
                "personality": {
                    "system_message": "Neutral",
                    "voice": "alloy",
                    "temperature": 0.5,
                },
                "turn_taking": {
                    "type": "speak_first",
                    "initial_delay": 1.0,
                    "initial_message": "Hello, testing.",
                },
            },
            "output_schema": valid_schema,
        },
    },
]


@pytest.mark.parametrize("valid_input", valid_cases)
def test_valid_call_request(valid_input):
    """Test that valid CallRequest instances are accepted."""
    call_request = CallRequest(**valid_input)
    assert call_request.contact is not None
    assert call_request.configuration.intent.description
    assert call_request.configuration.output_schema is not None


@pytest.mark.parametrize("invalid_input", invalid_cases)
def test_invalid_call_request(invalid_input):
    """Test that invalid CallRequest instances raise ValidationError."""
    with pytest.raises(ValidationError):
        CallRequest(**invalid_input)
