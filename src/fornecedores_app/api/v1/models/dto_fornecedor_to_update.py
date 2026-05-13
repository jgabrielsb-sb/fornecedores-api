from pydantic import BaseModel


class FornecedorToUpdateResponse(BaseModel):
    LOJA: str
    CODIGO: str
    NOME: str
    NOME_FANTASIA: str
    CPF_CNPJ: str
