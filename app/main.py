from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .routers import ws, api

app = FastAPI()
app.mount(path="/ws", app=ws.app)
app.mount(path="/api/v1", app=api.app)


@app.get("/health", response_class=JSONResponse)
async def healthcheck():
    return {"status": "ok"}
