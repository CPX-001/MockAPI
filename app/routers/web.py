from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.core.settings import TEMPLATES_DIR

router = APIRouter(prefix = "/web", tags = ["website"])

templates = Jinja2Templates(directory = TEMPLATES_DIR)

@router.get("/")
async def homepage(request:Request):
    return templates.TemplateResponse("home.html", {"request" : request})
    
@router.get("/create_endpoint_form")
def create_endpoint_form(request:Request):
    return templates.TemplateResponse("create_endpoint_form.html", {"request": request})