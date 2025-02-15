from fastapi import FastAPI
from starlette.middleware.authentication import AuthenticationMiddleware

from app.authn import BasicAuthBackend

from .calls import calls

app = FastAPI()
app.add_middleware(
    AuthenticationMiddleware,
    backend=BasicAuthBackend(["admin"]),
    on_error=BasicAuthBackend.on_auth_error,
)
app.mount("/calls", calls)
