from datetime import datetime, timezone

from sqlalchemy.orm import Session

from fornecedores_app.api.v1.models import dto_fornecedor
from fornecedores_app.db.schemas import FornecedoresSchema


def create(
    fornecedor: dto_fornecedor.FornecedorCreate,
    *,
    now: datetime,
    session: Session,
) -> FornecedoresSchema:
    db_fornecedor = FornecedoresSchema(
        cnpj=fornecedor.cnpj.value,
        created_at=now,
        updated_at=now,
    )
    session.add(db_fornecedor)
    session.flush()
    return db_fornecedor


def get_fornecedor_by_cnpj(cnpj: str, session: Session) -> FornecedoresSchema | None:
    return (
        session.query(FornecedoresSchema)
        .filter(FornecedoresSchema.cnpj == cnpj)
        .first()
    )


def get_by_id(fornecedor_id: int, session: Session) -> FornecedoresSchema | None:
    return (
        session.query(FornecedoresSchema)
        .filter(FornecedoresSchema.id == fornecedor_id)
        .first()
    )
