from typing import Annotated, Any, Generator

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fornecedores_app.api.v1.models import dto_logs, dto_responses
from fornecedores_app.api.v1.services import logs_service
from fornecedores_app.db.session import get_db

router = APIRouter(
    prefix="/logs",
    tags=["v1/logs"],
)


@router.post(
    "/",
    response_model=dto_logs.LogResponse,
    status_code=201,
    responses={
        422: {
            "description": "Unprocessable Entity",
            "model": dto_responses.Error422Response,
        },
    },
)
async def create_log(
    log_create: dto_logs.LogCreate,
    session: Generator[Session, Any, None] = Depends(get_db),
) -> dto_logs.LogResponse:
    return logs_service.create_log(log_create=log_create, session=session)


@router.get(
    "",
    response_model=dto_responses.PaginatedResponse[dto_logs.LogResponse],
    status_code=200,
    description=(
        "Retrieve logs with optional filtering by trace_id, process_name, status, date range, "
        "and metadata_json: either metadata_key + metadata_value, and/or metadata_match "
        "(JSON object of key/value pairs, all must match — AND)."
    ),
    responses={
        422: {
            "description": "Unprocessable Entity",
            "model": dto_responses.Error422Response,
        },
    },
)
async def get_logs(
    log_filter: Annotated[dto_logs.LogFilter, Depends()],
    session: Annotated[Session, Depends(get_db)],
) -> dto_responses.PaginatedResponse[dto_logs.LogResponse]:
    return logs_service.get_logs(log_filter=log_filter, session=session)


@router.get(
    "/{log_id}",
    response_model=dto_logs.LogResponse,
    status_code=200,
    responses={
        404: {
            "description": "Log not found",
            "model": dto_responses.Error404Response,
        },
    },
)
async def get_log(
    log_id: int,
    session: Generator[Session, Any, None] = Depends(get_db),
) -> dto_logs.LogResponse:
    return logs_service.get_log_by_id(log_id=log_id, session=session)
