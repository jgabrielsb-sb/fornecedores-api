from typing import Any, Generator

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fornecedores_app.api.v1.models import dto_fornecedor, dto_responses
from fornecedores_app.api.v1.services import fornecedor_service
from fornecedores_app.db.session import get_db

router = APIRouter(
    prefix="/fornecedores",
    tags=["v1/fornecedores"],
)


@router.post(
    "/",
    response_model=dto_fornecedor.FornecedorResponse,
    status_code=201,
    responses={
        400: {
            "description": "Bad Request",
            "model": dto_responses.Error400Response,
        },
        409: {
            "description": "Conflict",
            "model": dto_responses.Error409Response,
        },
        422: {
            "description": "Unprocessable Entity",
            "model": dto_responses.Error422Response,
        },
    },
)
async def create_fornecedor(
    fornecedor_create: dto_fornecedor.FornecedorCreate,
    session: Generator[Session, Any, None] = Depends(get_db),
) -> dto_fornecedor.FornecedorResponse:
    return fornecedor_service.create_fornecedor(
        fornecedor_create=fornecedor_create,
        session=session,
    )


@router.get(
    "/{fornecedor_id}",
    response_model=dto_fornecedor.FornecedorResponse,
    status_code=200,
    summary="Get fornecedor by id",
    responses={
        404: {
            "description": "Fornecedor not found",
            "model": dto_responses.Error404Response,
        },
        422: {
            "description": "Unprocessable Entity",
            "model": dto_responses.Error422Response,
        },
    },
)
async def get_fornecedor_by_id(
    fornecedor_id: int,
    session: Generator[Session, Any, None] = Depends(get_db),
) -> dto_fornecedor.FornecedorResponse:
    return fornecedor_service.get_fornecedor_by_id(
        fornecedor_id,
        session,
    )
