# Contiene operaciones de persistencia para schemas.
from sqlalchemy.orm import Session

from app.storage.models.schema import Schema


def create_schema(db: Session, schema: Schema):
    db.add(schema)
    db.commit()
    db.refresh(schema)

    return schema
