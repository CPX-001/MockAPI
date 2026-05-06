# Contiene operaciones de persistencia para endpoints mock.
from sqlalchemy.orm import Session

from app.storage.models.endpoint import Endpoint


def create_endpoint(db: Session, endpoint: Endpoint):
    db.add(endpoint)
    db.commit()
    db.refresh(endpoint)

    return endpoint
