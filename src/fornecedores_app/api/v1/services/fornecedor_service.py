from datetime import UTC, datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from fornecedores_app.api.v1.models import dto_fornecedor
from fornecedores_app.api.v1.repos import fornecedor_repo
from fornecedores_app.api.v1.services.exceptions import ConflictException, NotFoundException


def create_fornecedor(
    fornecedor_create: dto_fornecedor.FornecedorCreate,
    session: Session,
) -> dto_fornecedor.FornecedorResponse:
    existing = fornecedor_repo.get_fornecedor_by_cnpj(fornecedor_create.cnpj, session)
    if existing:
        raise ConflictException(
            resource="cnpj",
            identifier=fornecedor_create.cnpj,
            object="fornecedor",
        )

    try:
        now = datetime.now(UTC)
        db_fornecedor = fornecedor_repo.create(fornecedor_create, now=now, session=session)
        fornecedor_response = dto_fornecedor.FornecedorResponse.model_validate(db_fornecedor)
        session.commit()
        return fornecedor_response
    except IntegrityError:
        session.rollback()
        raise ConflictException(
            resource="cnpj",
            identifier=fornecedor_create.cnpj,
            object="fornecedor",
        ) from None

def get_fornecedor_by_cnpj(
    cnpj: str,
    session: Session,
) -> dto_fornecedor.FornecedorResponse:
    db_fornecedor = fornecedor_repo.get_fornecedor_by_cnpj(cnpj, session)
    if not db_fornecedor:
        raise NotFoundException(
            resource="cnpj",
            identifier=cnpj,
            object="fornecedor",
        )
    return dto_fornecedor.FornecedorResponse.model_validate(db_fornecedor)


def get_fornecedor_by_id(
    fornecedor_id: int,
    session: Session,
) -> dto_fornecedor.FornecedorResponse:
    db_fornecedor = fornecedor_repo.get_by_id(fornecedor_id, session)

    if not db_fornecedor:
        raise NotFoundException(
            resource="id",
            identifier=str(fornecedor_id),
            object="fornecedor",
        )

    return dto_fornecedor.FornecedorResponse.model_validate(db_fornecedor)
