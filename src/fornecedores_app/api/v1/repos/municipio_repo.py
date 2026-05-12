from datetime import datetime

from sqlalchemy.orm import Session

from fornecedores_app.api.v1.models.dto_municipio import MunicipioCreate
from fornecedores_app.db.schemas import MunicipiosSchema


def create(
    municipio: MunicipioCreate,
    *,
    now: datetime,
    session: Session,
) -> MunicipiosSchema:
    db_municipio = MunicipiosSchema(
        municipio_name=municipio.municipio_name,
        codigo_ibge=municipio.codigo_ibge,
        created_at=now,
        updated_at=now,
    )
    session.add(db_municipio)
    session.flush()
    return db_municipio


def get_by_id(municipio_id: int, session: Session) -> MunicipiosSchema | None:
    return (
        session.query(MunicipiosSchema)
        .filter(MunicipiosSchema.id == municipio_id)
        .first()
    )


def get_by_name(municipio_name: str, session: Session) -> MunicipiosSchema | None:
    return (
        session.query(MunicipiosSchema)
        .filter(MunicipiosSchema.municipio_name == municipio_name)
        .first()
    )


def get_by_codigo_ibge(codigo_ibge: str, session: Session) -> MunicipiosSchema | None:
    return (
        session.query(MunicipiosSchema)
        .filter(MunicipiosSchema.codigo_ibge == codigo_ibge)
        .first()
    )
