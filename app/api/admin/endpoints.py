# Expone rutas administrativas para registrar y gestionar endpoints mock.
from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from app.services.endpoint_registry import endpoint_response, register_endpoint
from app.storage.database import get_db

router = APIRouter(prefix="/endpoint", tags=["endpoint"])


@router.post("")
async def receive_endpoint(
    request: Request,
    db: Session = Depends(get_db),
):
    endpoint_data = await request.json()
    saved_endpoint = register_endpoint(db, endpoint_data)

    return endpoint_response(saved_endpoint)
