from pydantic import BaseModel, ValidationError
import pytest

from fornecedores_app.api.fields.cnpj_field import CNPJField, validate_cnpj

pytestmark = pytest.mark.unit


class _CNPJModel(BaseModel):
    cnpj: CNPJField


VALID_CNPJ_VARIATIONS = [
    "62.173.620/0001-80",
    "62.173.620/000180",
    "62173620000180",
    "62 173 620 0001 80",
    "62-173-620-0001-80",
    "62.173.620.0001.80",
    "62/173/620/0001/80",
    "62_173_620_0001_80",
    " 62.173.620/0001-80 ",
    " 62173620000180 ",
    "62.173.620 / 0001-80",
    "62 . 173 . 620 / 0001 - 80",
    "62.173.620/0001 - 80",
    "62.173.620 /0001-80",
    "62.173.620/ 0001-80",
    "62.173.620/0001- 80",
]

INVALID_CNPJS_WITH_EXTRA_DIGIT = [
    "62.173.620/0001-800",
    "62.173.620/0001800",
    "621736200001800",
    "62 173 620 0001 800",
    "62-173-620-0001-800",
    "62.173.620.0001.800",
    "62/173/620/0001/800",
    "62_173_620_0001_800",
    " 62.173.620/0001-800 ",
    " 621736200001800 ",
    "62.173.620 / 0001-800",
    "62 . 173 . 620 / 0001 - 800",
    "62.173.620/0001 - 800",
    "62.173.620 /0001-800",
    "62.173.620/ 0001-800",
    "62.173.620/0001- 800",
]

INVALID_CNPJS_WITH_MISSING_DIGIT = [
    "62.173.620/0001-8",
    "62.173.620/00018",
    "6217362000018",
    "62 173 620 0001 8",
    "62-173-620-0001-8",
    "62.173.620.0001.8",
    "62/173/620/0001/8",
    "62_173_620_0001_8",
    " 62.173.620/0001-8 ",
    " 6217362000018 ",
    "62.173.620 / 0001-8",
    "62 . 173 . 620 / 0001 - 8",
    "62.173.620/0001 - 8",
    "62.173.620 /0001-8",
    "62.173.620/ 0001-8",
    "62.173.620/0001- 8",
]

INVALID_LENGTH_CNPJS = INVALID_CNPJS_WITH_EXTRA_DIGIT + INVALID_CNPJS_WITH_MISSING_DIGIT


@pytest.mark.parametrize("cnpj", VALID_CNPJ_VARIATIONS)
def test_validate_cnpj_accepts_supported_formats(cnpj: str):
    assert validate_cnpj(cnpj) == "62173620000180"


@pytest.mark.parametrize("cnpj", VALID_CNPJ_VARIATIONS)
def test_cnpj_field_normalizes_to_digits(cnpj: str):
    model = _CNPJModel(cnpj=cnpj)
    assert model.cnpj == "62173620000180"


@pytest.mark.parametrize("cnpj", INVALID_LENGTH_CNPJS)
def test_cnpj_field_rejects_invalid_lengths(cnpj: str):
    with pytest.raises(ValidationError):
        _CNPJModel(cnpj=cnpj)
