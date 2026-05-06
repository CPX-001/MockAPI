# Registra endpoints mock a partir de datos leidos por la capa HTTP.
from typing import Any

from sqlalchemy.orm import Session

from app.storage.models.endpoint import Endpoint
from app.storage.models.schema import Schema
from app.storage.repositories.endpoint import create_endpoint


def schema_payload(endpoint_data: dict[str, Any]) -> Schema:
    return Schema(definition=endpoint_data.get("schema", {}))


def endpoint_payload(endpoint_data: dict[str, Any]) -> Endpoint:
    return Endpoint(
        method=endpoint_data.get("method"),
        path=endpoint_data.get("path"),
        schema=schema_payload(endpoint_data),
    )


def endpoint_response(endpoint: Endpoint) -> dict[str, Any]:
    return {
        "id": endpoint.id,
        "method": endpoint.method,
        "path": endpoint.path,
        "schema": endpoint.schema.definition,
    }


def register_endpoint(db: Session, endpoint_data: dict[str, Any]) -> Endpoint:
    endpoint = endpoint_payload(endpoint_data)
    return create_endpoint(db, endpoint)
