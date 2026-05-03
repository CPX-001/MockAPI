import asyncio
import json
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen


JsonDict = Dict[str, Any]


@dataclass
class ApiResponse:
    method: str
    url: str
    ok: bool
    status_code: Optional[int] = None
    data: Any = None
    text: str = ""
    error: Optional[str] = None


def build_url(base_url: str, path: str) -> str:
    base = base_url.rstrip("/") + "/"
    return urljoin(base, path.lstrip("/"))


def _decode(raw_body: bytes) -> str:
    return raw_body.decode("utf-8", errors="replace")


def _parse_body(response_text: str) -> Any:
    if not response_text:
        return None

    try:
        return json.loads(response_text)
    except ValueError:
        return None


def _send_json_request(
    *,
    method: str,
    url: str,
    payload: Optional[JsonDict],
    timeout: float,
    token: Optional[str],
) -> ApiResponse:
    headers = {"Accept": "application/json"}
    data = None

    if payload is not None:
        headers["Content-Type"] = "application/json"
        data = json.dumps(payload).encode("utf-8")

    if token:
        headers["Authorization"] = f"Bearer {token}"

    request = Request(url=url, data=data, headers=headers, method=method)

    try:
        with urlopen(request, timeout=timeout) as response:
            status_code = response.status
            response_text = _decode(response.read())
    except HTTPError as exc:
        status_code = exc.code
        response_text = _decode(exc.read())
    except (TimeoutError, URLError, OSError) as exc:
        return ApiResponse(
            method=method,
            url=url,
            ok=False,
            error=f"No se pudo contactar con la API: {exc}",
        )

    return ApiResponse(
        method=method,
        url=url,
        ok=200 <= status_code < 400,
        status_code=status_code,
        data=_parse_body(response_text),
        text=response_text,
    )


async def request_json(
    *,
    method: str,
    path: str,
    base_url: str,
    timeout: float,
    token: Optional[str] = None,
    payload: Optional[JsonDict] = None,
) -> ApiResponse:
    return await asyncio.to_thread(
        _send_json_request,
        method=method.upper(),
        url=build_url(base_url, path),
        payload=payload,
        timeout=timeout,
        token=token,
    )


def normalize_ticket_list(data: Any) -> List[JsonDict]:
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]

    if isinstance(data, dict):
        for key in ("items", "tickets", "data", "results"):
            items = data.get(key)
            if isinstance(items, list):
                return [item for item in items if isinstance(item, dict)]

    return []


def normalize_ticket(data: Any) -> JsonDict:
    if isinstance(data, dict):
        return data
    return {}


def ticket_id(ticket: JsonDict) -> str:
    value = ticket.get("id") or ticket.get("_id") or ticket.get("uuid")
    return str(value) if value is not None else ""
