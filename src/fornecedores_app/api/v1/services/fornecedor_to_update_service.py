from sqlalchemy.orm import Session

from fornecedores_app.api.v1.models.dto_fornecedor_to_update import FornecedorToUpdateResponse
from fornecedores_app.api.v1.repos import fornecedor_to_update_repo


def get(session: Session) -> list[FornecedorToUpdateResponse]:
    return fornecedor_to_update_repo.get(session)
