
from pydantic import BaseModel, ConfigDict
from datetime import datetime

from fornecedores_app.api.fields import CEPField

class FornecedorOnProtheusVersion0Create(BaseModel):
    id_fornecedor: int

class FornecedorOnProtheusUpdate(BaseModel):
    cep: CEPField

class FornecedorOnProtheusResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    id_fornecedor: int
    cep: CEPField | None
    version: int
    to_update: bool
    protheus_synced_version: int
    protheus_last_synced_at: datetime | None
    created_at: datetime
    updated_at: datetime