from datetime import UTC, datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fornecedores_app.api.v1.models.dto_municipio import MunicipioCreate, MunicipioResponse
from fornecedores_app.api.v1.repos import municipio_repo
from fornecedores_app.api.v1.services.exceptions import ConflictException, NotFoundException


def create_municipio(
    municipio_create: MunicipioCreate,
    session: Session,
) -> MunicipioResponse:
    existing = municipio_repo.get_by_codigo_ibge(municipio_create.codigo_ibge, session)
    if existing:
        raise ConflictException(
            resource="codigo_ibge",
            identifier=municipio_create.codigo_ibge,
            object="municipio",
        )

    try:
        now = datetime.now(UTC)
        db_municipio = municipio_repo.create(municipio_create, now=now, session=session)
        municipio_response = MunicipioResponse.model_validate(db_municipio)
        session.commit()
        return municipio_response
    except IntegrityError:
        session.rollback()
        raise ConflictException(
            resource="codigo_ibge",
            identifier=municipio_create.codigo_ibge,
            object="municipio",
        ) from None


def get_municipio_by_id(
    municipio_id: int,
    session: Session,
) -> MunicipioResponse:
    db_municipio = municipio_repo.get_by_id(municipio_id, session)
    if not db_municipio:
        raise NotFoundException(
            resource="id",
            identifier=str(municipio_id),
            object="municipio",
        )
    return MunicipioResponse.model_validate(db_municipio)


def get_municipio_by_name(
    municipio_name: str,
    session: Session,
) -> MunicipioResponse:
    db_municipio = municipio_repo.get_by_name(municipio_name, session)
    if not db_municipio:
        raise NotFoundException(
            resource="municipio_name",
            identifier=municipio_name,
            object="municipio",
        )
    return MunicipioResponse.model_validate(db_municipio)


def get_municipio_by_codigo_ibge(
    codigo_ibge: str,
    session: Session,
) -> MunicipioResponse:
    db_municipio = municipio_repo.get_by_codigo_ibge(codigo_ibge, session)
    if not db_municipio:
        raise NotFoundException(
            resource="codigo_ibge",
            identifier=codigo_ibge,
            object="municipio",
        )
    return MunicipioResponse.model_validate(db_municipio)
