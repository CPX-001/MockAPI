from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from client_app.api_client import (
    ApiResponse,
    normalize_ticket,
    normalize_ticket_list,
    request_json,
    ticket_id,
)
from client_app.config import get_settings


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Service Desk")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

templates = Jinja2Templates(directory=BASE_DIR / "templates")
templates.env.globals["ticket_id"] = ticket_id


def page_context(request: Request, **extra: object) -> dict:
    context = {
        "request": request,
        "settings": get_settings(),
    }
    context.update(extra)
    return context


def ticket_payload(
    *,
    title: str,
    customer: str,
    priority: str,
    status: str,
    description: str,
) -> dict:
    return {
        "title": title,
        "customer": customer,
        "priority": priority,
        "status": status,
        "description": description,
    }


async def api_call(method: str, path: str, payload: Optional[dict] = None) -> ApiResponse:
    settings = get_settings()
    return await request_json(
        method=method,
        path=path,
        payload=payload,
        base_url=settings.api_base_url,
        timeout=settings.request_timeout,
        token=settings.api_token,
    )


@app.get("/", response_class=HTMLResponse, name="tickets_index")
async def tickets_index(request: Request):
    response = await api_call("GET", "/tickets")
    tickets = normalize_ticket_list(response.data)

    return templates.TemplateResponse(
        "tickets/index.html",
        page_context(
            request,
            tickets=tickets,
            api_response=response,
            total_open=sum(1 for ticket in tickets if ticket.get("status") != "closed"),
            total_critical=sum(1 for ticket in tickets if ticket.get("priority") == "critical"),
        ),
    )


@app.get("/tickets/new", response_class=HTMLResponse, name="ticket_new")
async def ticket_new(request: Request):
    return templates.TemplateResponse(
        "tickets/form.html",
        page_context(
            request,
            mode="create",
            ticket={},
            api_response=None,
        ),
    )


@app.post("/tickets", response_class=HTMLResponse, name="ticket_create")
async def ticket_create(
    request: Request,
    title: str = Form(...),
    customer: str = Form(...),
    priority: str = Form(...),
    status: str = Form(...),
    description: str = Form(""),
):
    payload = ticket_payload(
        title=title,
        customer=customer,
        priority=priority,
        status=status,
        description=description,
    )
    response = await api_call("POST", "/tickets", payload)

    if response.ok:
        return RedirectResponse(url=request.url_for("tickets_index"), status_code=303)

    return templates.TemplateResponse(
        "tickets/form.html",
        page_context(
            request,
            mode="create",
            ticket=payload,
            api_response=response,
        ),
        status_code=400,
    )


@app.get("/tickets/{item_id}", response_class=HTMLResponse, name="ticket_detail")
async def ticket_detail(request: Request, item_id: str):
    response = await api_call("GET", f"/tickets/{item_id}")
    ticket = normalize_ticket(response.data)

    return templates.TemplateResponse(
        "tickets/detail.html",
        page_context(
            request,
            item_id=item_id,
            ticket=ticket,
            api_response=response,
        ),
    )


@app.get("/tickets/{item_id}/edit", response_class=HTMLResponse, name="ticket_edit")
async def ticket_edit(request: Request, item_id: str):
    response = await api_call("GET", f"/tickets/{item_id}")
    ticket = normalize_ticket(response.data)

    return templates.TemplateResponse(
        "tickets/form.html",
        page_context(
            request,
            mode="edit",
            item_id=item_id,
            ticket=ticket,
            api_response=response if not response.ok else None,
        ),
    )


@app.post("/tickets/{item_id}", response_class=HTMLResponse, name="ticket_update")
async def ticket_update(
    request: Request,
    item_id: str,
    title: str = Form(...),
    customer: str = Form(...),
    priority: str = Form(...),
    status: str = Form(...),
    description: str = Form(""),
):
    payload = ticket_payload(
        title=title,
        customer=customer,
        priority=priority,
        status=status,
        description=description,
    )
    response = await api_call("PUT", f"/tickets/{item_id}", payload)

    if response.ok:
        return RedirectResponse(url=request.url_for("ticket_detail", item_id=item_id), status_code=303)

    return templates.TemplateResponse(
        "tickets/form.html",
        page_context(
            request,
            mode="edit",
            item_id=item_id,
            ticket=payload,
            api_response=response,
        ),
        status_code=400,
    )


@app.post("/tickets/{item_id}/delete", response_class=HTMLResponse, name="ticket_delete")
async def ticket_delete(request: Request, item_id: str):
    response = await api_call("DELETE", f"/tickets/{item_id}")

    if response.ok:
        return RedirectResponse(url=request.url_for("tickets_index"), status_code=303)

    return templates.TemplateResponse(
        "tickets/detail.html",
        page_context(
            request,
            item_id=item_id,
            ticket={"id": item_id},
            api_response=response,
        ),
        status_code=400,
    )
