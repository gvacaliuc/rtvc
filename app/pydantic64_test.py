from pydantic import BaseModel

from .pydantic64 import encode, decode

# Example Usage:
class Address(BaseModel):
    street: str
    city: str

class User(BaseModel):
    name: str
    age: int
    address: Address

def test_bijection():
    user = User(name="John Doe", age=30, address=Address(street="123 Main St", city="Springfield"))

    # Serialize
    encoded = encode(user)
    decoded = decode(encoded, klass=User)

    assert user == decoded
