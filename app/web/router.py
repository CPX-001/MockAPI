# Renderiza las paginas HTML de administracion de MockAPI.
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.core.settings import Settings

router = APIRouter(prefix = "/web", tags = ["website"])
settings = Settings()

templates = Jinja2Templates(directory = settings.templates_dir)

@router.get("/")
async def homepage(request:Request):
    return templates.TemplateResponse(request, "home.html")

@router.get("/create_endpoint_form")
def create_endpoint_form(request:Request):
    return templates.TemplateResponse(request, "create_endpoint_form.html")
