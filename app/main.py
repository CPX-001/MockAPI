# Crea la aplicacion FastAPI, inicializa recursos y registra routers.
from contextlib import asynccontextmanager

from app.routing import router as app_routing
from app.storage.database import init_db
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)
app.include_router(app_routing)

@app.get("/")
async def web_redirect(request: Request):
    return RedirectResponse(url="/web", status_code=302)
