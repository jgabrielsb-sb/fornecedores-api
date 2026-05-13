from typing import Any, Generator

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from fornecedores_app.api.v1.models.dto_fornecedor_to_update import FornecedorToUpdateResponse
from fornecedores_app.api.v1.services import fornecedor_to_update_service
from fornecedores_app.db.mp12_session import get_db

router = APIRouter(
    prefix="/fornecedores-to-update",
    tags=["v1/fornecedores-to-update"],
)


@router.get(
    "/",
    response_model=list[FornecedorToUpdateResponse],
    status_code=200,
    summary="Get fornecedores pending update from Protheus",
)
async def get_fornecedores_to_update(
    session: Generator[Session, Any, None] = Depends(get_db),
) -> list[FornecedorToUpdateResponse]:
    return fornecedor_to_update_service.get(session=session)
