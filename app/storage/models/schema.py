# Define la tabla que guarda definiciones JSON de schemas.
from sqlalchemy import Integer, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.storage.database import Base

class Schema(Base):
    __tablename__ = "schemas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    definition: Mapped[dict] = mapped_column(JSON, nullable=False)

    endpoints: Mapped[list["Endpoint"]] = relationship(
        "Endpoint",
        back_populates = "schema"
    )
