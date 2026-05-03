from pathlib import Path

from fastapi.responses import RedirectResponse
from app.core.settings import TEMPLATES_DIR
from fastapi import FastAPI, Request, Response
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.routers import web

app = FastAPI()

app.include_router(web.router)

@app.get("/")
async def web_redirect(request:Request):
    return RedirectResponse(url = request.url_for("homepage"))