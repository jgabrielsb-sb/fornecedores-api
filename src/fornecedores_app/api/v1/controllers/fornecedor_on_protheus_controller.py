from datetime import UTC, datetime
from typing import Any, Generator

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fornecedores_app.api.v1.models import dto_fornecedor_on_protheus, dto_responses
from fornecedores_app.api.v1.services import fornecedor_on_protheus_service
from fornecedores_app.db.session import get_db

router = APIRouter(
    prefix="/fornecedores-on-protheus",
    tags=["v1/fornecedores-on-protheus"],
)


@router.patch(
    "/{id}",
    response_model=dto_fornecedor_on_protheus.FornecedorOnProtheusResponse,
    status_code=200,
    responses={
        403: {
            "description": "Update not allowed because to_update is false",
            "model": dto_responses.Error403Response,
        },
        404: {
            "description": "Fornecedor on Protheus not found",
            "model": dto_responses.Error404Response,
        },
        422: {
            "description": "Unprocessable Entity",
            "model": dto_responses.Error422Response,
        },
    },
)
async def update_fornecedor_on_protheus(
    id: int,
    fornecedor_on_protheus: dto_fornecedor_on_protheus.FornecedorOnProtheusUpdate,
    session: Generator[Session, Any, None] = Depends(get_db),
) -> dto_fornecedor_on_protheus.FornecedorOnProtheusResponse:
    return fornecedor_on_protheus_service.update(
        id=id,
        fornecedor_on_protheus=fornecedor_on_protheus,
        now=datetime.now(UTC),
        session=session,
    )


@router.post(
    "/{id}/sync",
    response_model=dto_fornecedor_on_protheus.FornecedorOnProtheusResponse,
    status_code=200,
    responses={
        404: {
            "description": "Fornecedor on Protheus not found",
            "model": dto_responses.Error404Response,
        },
        422: {
            "description": "Unprocessable Entity",
            "model": dto_responses.Error422Response,
        },
    },
)
async def sync_fornecedor_on_protheus(
    id: int,
    session: Generator[Session, Any, None] = Depends(get_db),
) -> dto_fornecedor_on_protheus.FornecedorOnProtheusResponse:
    return fornecedor_on_protheus_service.sync_protheus_synced_version(
        id=id,
        now=datetime.now(UTC),
        session=session,
    )


@router.post(
    "/{id}/mark-for-update",
    response_model=dto_fornecedor_on_protheus.FornecedorOnProtheusResponse,
    status_code=200,
    responses={
        404: {
            "description": "Fornecedor on Protheus not found",
            "model": dto_responses.Error404Response,
        },
        422: {
            "description": "Unprocessable Entity",
            "model": dto_responses.Error422Response,
        },
    },
)
async def mark_fornecedor_on_protheus_for_update(
    id: int,
    session: Generator[Session, Any, None] = Depends(get_db),
) -> dto_fornecedor_on_protheus.FornecedorOnProtheusResponse:
    return fornecedor_on_protheus_service.set_to_update_to_true(
        id=id,
        session=session,
    )
