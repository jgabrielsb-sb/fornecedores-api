from datetime import datetime, timezone

from sqlalchemy.orm import Session

from fornecedores_app.api.v1.repos import fornecedor_on_protheus_repo
from fornecedores_app.api.v1.models import dto_fornecedor, dto_fornecedor_on_protheus
from fornecedores_app.db.schemas import FornecedoresSchema



def create(
    fornecedor: dto_fornecedor.FornecedorCreate,
    *,
    now: datetime,
    session: Session,
) -> FornecedoresSchema:
    db_fornecedor = FornecedoresSchema(
        cnpj=fornecedor.cnpj,
        created_at=now,
        updated_at=now,
    )
    session.add(db_fornecedor)
    session.flush()
    
    # Create fornecedor on protheus version 0
    fornecedor_on_protheus_repo.create_version_0(
        fornecedor_on_protheus=dto_fornecedor_on_protheus.FornecedorOnProtheusVersion0Create(
            id_fornecedor=db_fornecedor.id,
        ),
        now=now,
        session=session,
    )
    
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
