from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from fornecedores_app.api.fields.codigo_ibge_field import CodigoIBGEField


class MunicipioCreate(BaseModel):
    """Payload to create a municipio."""

    municipio_name: str = Field(..., description="Municipality name")
    codigo_ibge: CodigoIBGEField = Field(..., description="IBGE municipality code (digits or formatted)")


class MunicipioResponse(BaseModel):
    """Municipio returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., description="The municipio id")
    municipio_name: str = Field(..., description="Municipality name")
    codigo_ibge: CodigoIBGEField = Field(..., description="IBGE municipality code")
    created_at: datetime = Field(..., description="Creation timestamp (UTC)")
    updated_at: datetime = Field(..., description="Last update timestamp (UTC)")
