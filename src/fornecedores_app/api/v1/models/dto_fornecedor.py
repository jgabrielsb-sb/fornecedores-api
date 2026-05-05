from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from fornecedores_app.domain.value_objects import CNPJ


class FornecedorCreate(BaseModel):
    """Payload to create a fornecedor."""

    cnpj: CNPJ = Field(..., description="CNPJ (digits or formatted)")


class FornecedorResponse(BaseModel):
    """Fornecedor returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="The fornecedor id")
    cnpj: CNPJ = Field(..., description="CNPJ")
    created_at: datetime = Field(..., description="Creation timestamp (UTC)")
    updated_at: datetime = Field(..., description="Last update timestamp (UTC)")
