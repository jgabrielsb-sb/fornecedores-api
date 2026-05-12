import pytest
from pydantic import BaseModel, ValidationError

from fornecedores_app.api.fields.codigo_ibge_field import CodigoIBGEField, validate_codigo_ibge

pytestmark = pytest.mark.unit


class _CodigoIBGEModel(BaseModel):
    codigo_ibge: CodigoIBGEField


VALID_CODIGO_IBGE_VARIATIONS = [
    "1200013",
    "1200013 ",
    " 1200013",
    " 1200013 ",
    "120 0013",
    "120-0013",
    "120.0013",
    "120/0013",
    "120_0013",
    "12 00013",
    "1200 013",
    "1 200013",
    "12.00013",
    "12-00013",
    "12/00013",
    "12_00013",
]

INVALID_CODIGO_IBGE_WITH_EXTRA_DIGIT = [
    "12000130",
    " 12000130 ",
    "120 00130",
    "120-00130",
    "120.00130",
    "120/00130",
    "120_00130",
    "12 000 130",
    "12-000-130",
    "12.000.130",
    "12/000/130",
]

INVALID_CODIGO_IBGE_WITH_MISSING_DIGIT = [
    "120001",
    " 120001 ",
    "120 001",
    "120-001",
    "120.001",
    "120/001",
    "120_001",
    "12 000 1",
    "12-000-1",
    "12.000.1",
    "12/000/1",
]

INVALID_LENGTH_CODIGOS_IBGE = (
    INVALID_CODIGO_IBGE_WITH_EXTRA_DIGIT + INVALID_CODIGO_IBGE_WITH_MISSING_DIGIT
)


@pytest.mark.parametrize("ibge_input", VALID_CODIGO_IBGE_VARIATIONS)
def test_validate_codigo_ibge_accepts_supported_formats(ibge_input: str):
    assert validate_codigo_ibge(ibge_input) == "1200013"


@pytest.mark.parametrize("ibge_input", VALID_CODIGO_IBGE_VARIATIONS)
def test_codigo_ibge_field_normalizes_to_digits(ibge_input: str):
    model = _CodigoIBGEModel(codigo_ibge=ibge_input)
    assert model.codigo_ibge == "1200013"


@pytest.mark.parametrize("ibge_input", INVALID_LENGTH_CODIGOS_IBGE)
def test_codigo_ibge_field_rejects_invalid_lengths(ibge_input: str):
    with pytest.raises(ValidationError):
        _CodigoIBGEModel(codigo_ibge=ibge_input)
