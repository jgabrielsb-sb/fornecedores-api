from typing import Any, Generator

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fornecedores_app.api.v1.models import dto_responses
from fornecedores_app.api.v1.models.dto_municipio import MunicipioCreate, MunicipioResponse
from fornecedores_app.api.v1.services import municipio_service
from fornecedores_app.db.session import get_db

router = APIRouter(
    prefix="/municipios",
    tags=["v1/municipios"],
)


@router.post(
    "/",
    response_model=MunicipioResponse,
    status_code=201,
    responses={
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
async def create_municipio(
    municipio_create: MunicipioCreate,
    session: Generator[Session, Any, None] = Depends(get_db),
) -> MunicipioResponse:
    return municipio_service.create_municipio(
        municipio_create=municipio_create,
        session=session,
    )


@router.get(
    "/name/{municipio_name}",
    response_model=MunicipioResponse,
    status_code=200,
    summary="Get municipio by name",
    responses={
        404: {
            "description": "Municipio not found",
            "model": dto_responses.Error404Response,
        },
    },
)
async def get_municipio_by_name(
    municipio_name: str,
    session: Generator[Session, Any, None] = Depends(get_db),
) -> MunicipioResponse:
    return municipio_service.get_municipio_by_name(municipio_name, session)


@router.get(
    "/ibge/{codigo_ibge}",
    response_model=MunicipioResponse,
    status_code=200,
    summary="Get municipio by IBGE code",
    responses={
        404: {
            "description": "Municipio not found",
            "model": dto_responses.Error404Response,
        },
    },
)
async def get_municipio_by_codigo_ibge(
    codigo_ibge: str,
    session: Generator[Session, Any, None] = Depends(get_db),
) -> MunicipioResponse:
    return municipio_service.get_municipio_by_codigo_ibge(codigo_ibge, session)


@router.get(
    "/{municipio_id}",
    response_model=MunicipioResponse,
    status_code=200,
    summary="Get municipio by id",
    responses={
        404: {
            "description": "Municipio not found",
            "model": dto_responses.Error404Response,
        },
        422: {
            "description": "Unprocessable Entity",
            "model": dto_responses.Error422Response,
        },
    },
)
async def get_municipio_by_id(
    municipio_id: int,
    session: Generator[Session, Any, None] = Depends(get_db),
) -> MunicipioResponse:
    return municipio_service.get_municipio_by_id(municipio_id, session)
