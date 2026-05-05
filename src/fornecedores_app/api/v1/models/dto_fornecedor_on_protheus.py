
from pydantic import BaseModel

from fornecedores_app.api.fields import CEPField

class FornecedorOnProtheusVersion0Create(BaseModel):
    id_fornecedor: int

class FornecedorOnProtheusUpdate(BaseModel):
    cep: CEPField