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

def get_fornecedor_on_protheus_by_fornecedor_id(id_fornecedor: int, session: Session) -> FornecedorOnProteusSchema:
    return (
        session.query(FornecedorOnProteusSchema)
        .filter(FornecedorOnProteusSchema.id_fornecedor == id_fornecedor)
        .first()
    )


def update_fornecedor_on_protheus(
    *,
    id: int,
    fornecedor_on_protheus: FornecedorOnProtheusUpdate,
    now: datetime,
    session: Session,
) -> FornecedorOnProteusSchema:
    db_fornecedor_on_protheus = get_fornecedor_on_protheus_by_id(id, session)
    if db_fornecedor_on_protheus is None:
        raise ValueError("Fornecedor on protheus not found")
    
    db_fornecedor_on_protheus.cep = fornecedor_on_protheus.cep
    db_fornecedor_on_protheus.updated_at = now
    db_fornecedor_on_protheus.version += 1
    session.add(db_fornecedor_on_protheus)
    session.flush()
    return db_fornecedor_on_protheus

def sync_protheus_synced_version(
    *,
    id: int,
    now: datetime,
    session: Session,
) -> FornecedorOnProteusSchema:
    db_fornecedor_on_protheus = get_fornecedor_on_protheus_by_id(id, session)
    if not db_fornecedor_on_protheus.protheus_synced_version == db_fornecedor_on_protheus.version:
        db_fornecedor_on_protheus.protheus_synced_version = db_fornecedor_on_protheus.version
        db_fornecedor_on_protheus.protheus_last_synced_at = now
    
    session.add(db_fornecedor_on_protheus)
    session.flush()
    return db_fornecedor_on_protheus

def set_to_update_to_false(
    *,
    id: int,
    session: Session,
) -> FornecedorOnProteusSchema:
    db_fornecedor_on_protheus = get_fornecedor_on_protheus_by_id(id, session)
    if db_fornecedor_on_protheus is None:
        raise ValueError("Fornecedor on protheus not found")
    db_fornecedor_on_protheus.to_update = False
    session.add(db_fornecedor_on_protheus)
    session.flush()
    return db_fornecedor_on_protheus


def set_to_update_to_true(
    *,
    id: int,
    session: Session,
) -> FornecedorOnProteusSchema:
    db_fornecedor_on_protheus = get_fornecedor_on_protheus_by_id(id, session)
    if db_fornecedor_on_protheus is None:
        raise ValueError("Fornecedor on protheus not found")
    db_fornecedor_on_protheus.to_update = True
    session.add(db_fornecedor_on_protheus)
    session.flush()
    return db_fornecedor_on_protheus