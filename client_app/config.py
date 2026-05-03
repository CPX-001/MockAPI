import os
from dataclasses import dataclass
from functools import lru_cache
from typing import Optional


@dataclass(frozen=True)
class Settings:
    app_title: str = "Service Desk"
    api_base_url: str = "http://127.0.0.1:8000/api"
    api_token: Optional[str] = None
    request_timeout: float = 8.0


def _float_from_env(name: str, default: float) -> float:
    raw_value = os.getenv(name)
    if raw_value is None:
        return default

    try:
        return float(raw_value)
    except ValueError:
        return default


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_title=os.getenv("CLIENT_APP_TITLE", Settings.app_title),
        api_base_url=os.getenv("CLIENT_API_BASE_URL", Settings.api_base_url),
        api_token=os.getenv("CLIENT_API_TOKEN"),
        request_timeout=_float_from_env("CLIENT_REQUEST_TIMEOUT", Settings.request_timeout),
    )
