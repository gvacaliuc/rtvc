from typing import Optional, Tuple
import bcrypt
import secrets

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, Response
from starlette.authentication import (
    AuthCredentials, AuthenticationBackend, AuthenticationError, BaseUser, SimpleUser
)
from starlette.requests import HTTPConnection
from starlette.responses import PlainTextResponse
from starlette.routing import Route
import base64
import binascii

from .config import users_db

class UnauthorizedError(AuthenticationError):
    pass


class BasicAuthBackend(AuthenticationBackend):
    async def authenticate(self, conn):
        if "Authorization" not in conn.headers:
            raise UnauthorizedError("No authentication provided.")

        auth = conn.headers["Authorization"]
        try:
            scheme, credentials = auth.split()
            if scheme.lower() != 'basic':
                raise UnauthorizedError("No authentication provided.")
            decoded = base64.b64decode(credentials).decode("ascii")
        except (ValueError, UnicodeDecodeError, binascii.Error):
            raise UnauthorizedError("Invalid credential format.")

        username, _, password = decoded.partition(":")

        return _authenticate(username, password)

    @staticmethod
    def on_auth_error(_: HTTPConnection, exc: Exception) -> Response:
        assert isinstance(exc, UnauthorizedError), "unrecognized auth error"
        return JSONResponse({"error": str(exc)}, status_code=401)

def _authenticate(username: str, password: str) -> Tuple[AuthCredentials, BaseUser]:
    for cu, cpw in users_db.items():
        if secrets.compare_digest(cu, username) and bcrypt.checkpw(password.encode(), cpw.encode()):
            return AuthCredentials([]), SimpleUser(username)

    raise UnauthorizedError(f"Invalid credentials.")
