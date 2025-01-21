from fastapi import FastAPI
from fastapi.responses import JSONResponse

from .routers import ws, api

# TODO: subapplications + mounts might actually be more appropriate, not sure
app = FastAPI()
app.include_router(ws.router)
app.include_router(api.router, prefix="/api/v1")

@app.get('/health', response_class=JSONResponse)
async def healthcheck():
    return {"status": "ok"}
