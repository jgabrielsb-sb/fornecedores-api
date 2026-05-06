from datetime import datetime
from sqlalchemy.orm import Session

from fornecedores_app.api.v1.repos import fornecedor_on_protheus_repo
from fornecedores_app.api.v1.models import (
    FornecedorOnProtheusUpdate, 
    FornecedorOnProtheusResponse
)

from fornecedores_app.api.v1.services.exceptions import (
    NotFoundException, 
    ForbiddenException
)

def update(
    *,
    id: int,
    fornecedor_on_protheus: FornecedorOnProtheusUpdate,
    now: datetime,
    session: Session,
):
    # check if fornecedor on protheus exists
    row = fornecedor_on_protheus_repo.get_fornecedor_on_protheus_by_id(id, session)
    if row is None:
        raise NotFoundException(
            resource="fornecedor_on_protheus",
            identifier=id,
            object="fornecedor_on_protheus",
        )

    # check if to_update is true
    if not row.to_update:
        raise ForbiddenException(
            message="Fornecedor on protheus is not ready to be updated because to_update is false"
        )

    # update fornecedor on protheus
    row = fornecedor_on_protheus_repo.update_fornecedor_on_protheus(
        id=id,
        fornecedor_on_protheus=fornecedor_on_protheus,
        now=now,
        session=session,
    )

    # set to_update to false
    fornecedor_on_protheus_repo.set_to_update_to_false(
        id=id,
        session=session,
    )
    session.commit()
    return FornecedorOnProtheusResponse.model_validate(row)


def sync_protheus_synced_version(
    *,
    id: int,
    now: datetime,
    session: Session,
):
    row = fornecedor_on_protheus_repo.get_fornecedor_on_protheus_by_id(id, session)
    if row is None:
        raise NotFoundException(
            resource="fornecedor_on_protheus",
            identifier=id,
            object="fornecedor_on_protheus",
        )

    row = fornecedor_on_protheus_repo.sync_protheus_synced_version(
        id=id,
        now=now,
        session=session,
    )
    session.commit()
    return FornecedorOnProtheusResponse.model_validate(row)


def set_to_update_to_true(
    *,
    id: int,
    session: Session,
):
    row = fornecedor_on_protheus_repo.get_fornecedor_on_protheus_by_id(id, session)
    if row is None:
        raise NotFoundException(
            resource="fornecedor_on_protheus",
            identifier=id,
            object="fornecedor_on_protheus",
        )

    row = fornecedor_on_protheus_repo.set_to_update_to_true(
        id=id,
        session=session,
    )
    session.commit()
    return FornecedorOnProtheusResponse.model_validate(row)
