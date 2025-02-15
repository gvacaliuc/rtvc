import pytest
from pydantic import ValidationError
from .call import Behavior, CallIntent, Personality, VoiceCallConfiguration


def test_call_intent_creation():
    intent = CallIntent(description="Test Call", goal="Ensure validation works")
    assert intent.description == "Test Call"
    assert intent.goal == "Ensure validation works"


def test_voice_call_configuration_valid():
    schema = {
        "type": "object",
        "properties": {"name": {"type": "string"}, "age": {"type": "integer"}},
        "required": ["name"],
    }

    config = VoiceCallConfiguration(
        intent=CallIntent(
            description="Help desk support", goal="Resolve technical issues"
        ),
        behavior=Behavior(
            personality=Personality(system_message="talk like a pirate"),
            turn_taking=Behavior.Wait(),
        ),
        output_schema=schema,
    )

    assert config.intent.description == "Help desk support"
    assert config.intent.goal == "Resolve technical issues"
    assert config.output_schema == schema


def test_voice_call_configuration_invalid_schema():
    invalid_schema = {
        "type": "object",
        "properties": {"name": "invalid_type"},
    }  # Incorrect JSON schema type

    with pytest.raises(ValueError, match="Invalid JSON Schema"):
        VoiceCallConfiguration(
            intent=CallIntent(
                description="Help desk support", goal="Resolve technical issues"
            ),
            behavior=Behavior(
                personality=Personality(system_message="talk like a pirate"),
                turn_taking=Behavior.Wait(),
            ),
            output_schema=invalid_schema,
        )


def test_turn_taking_invalid_variant():
    with pytest.raises(ValidationError):
        Behavior(value={"type": "invalid"})  # type: ignore


def test_missing_required_fields():
    with pytest.raises(ValidationError):
        VoiceCallConfiguration(
            behavior=Behavior(
                personality=Personality(system_message="talk like a pirate"),
                turn_taking=Behavior.Wait(),
            ),
        )  # type: ignore


if __name__ == "__main__":
    pytest.main()
