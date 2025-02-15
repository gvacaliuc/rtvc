import base64
from typing import Type, TypeVar
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


def encode(model: BaseModel) -> str:
    """Serialize a Pydantic model to a base64-encoded JSON string."""
    json_data = model.model_dump_json()  # Use Pydantic's built-in JSON serialization
    return base64.urlsafe_b64encode(json_data.encode()).decode()


def decode(encoded: str, klass: Type[T]) -> T:
    """Deserialize a base64-encoded JSON string back to a Pydantic model."""
    json_data = base64.urlsafe_b64decode(encoded.encode()).decode()
    return klass.model_validate_json(json_data)
