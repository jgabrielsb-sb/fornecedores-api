from fornecedores_app.db.schemas import FornecedorOnProteusSchema
from fornecedores_app.api.v1.models import (
    FornecedorOnProtheusVersion0Create,
    FornecedorOnProtheusUpdate,
)

from datetime import datetime
from sqlalchemy.orm import Session

def create_version_0(
    fornecedor_on_protheus: FornecedorOnProtheusVersion0Create,
    *,
    now: datetime,
    session: Session
):
    db_fornecedor_on_protheus = FornecedorOnProteusSchema(
        **fornecedor_on_protheus.model_dump(mode='json'),
        created_at=now,
        updated_at=now,
    )
    session.add(db_fornecedor_on_protheus)
    session.flush()
    return db_fornecedor_on_protheus

def get_fornecedor_on_protheus_by_id(id: int, session: Session) -> FornecedorOnProteusSchema:
    return (
        session.query(FornecedorOnProteusSchema)
        .filter(FornecedorOnProteusSchema.id == id)
        .first()
    )


