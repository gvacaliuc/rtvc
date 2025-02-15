from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .routers import ws
from .routers.api import v1 as apiv1

app = FastAPI()
app.mount(path="/ws", app=ws.app)
app.mount(path="/api/v1", app=apiv1.app)


@app.get("/health", response_class=JSONResponse)
async def healthcheck():
    return {"status": "ok"}
