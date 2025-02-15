from jsonschema import Draft7Validator, SchemaError
from referencing.jsonschema import Schema as JSONSchema


def validate_jsonschema(schema: JSONSchema) -> JSONSchema:
    try:
        Draft7Validator.check_schema(schema)
    except SchemaError as e:
        raise ValueError(f"Invalid JSON Schema: {e}")
    return schema
