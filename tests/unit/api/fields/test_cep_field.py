import pytest
from pydantic import BaseModel, ValidationError

from fornecedores_app.api.fields.cep_field import CEPField, validate_cep


class _CEPModel(BaseModel):
    cep: CEPField


VALID_CEP_VARIATIONS = [
    "57020-565",
    "57020565",
    "57020 565",
    "57020.565",
    "57020/565",
    "57020_565",
    "57020-565 ",
    " 57020-565",
    " 57020-565 ",
    "57020 - 565",
    "57020- 565",
    "57020 -565",
    "57.020-565",
    "57 020 565",
    "57-020-565",
    "57/020/565",
]

INVALID_CEP_VARIATIONS_WITH_EXTRA_DIGIT = [
    "57020-5650",
    "570205650",
    "57020 5650",
    "57020.5650",
    "57020/5650",
    "57020_5650",
    "57020-5650 ",
    " 57020-5650",
    " 57020-5650 ",
    "57020 - 5650",
    "57020- 5650",
    "57020 -5650",
    "57.020-5650",
    "57 020 5650",
    "57-020-5650",
    "57/020/5650",
]

INVALID_CEP_VARIATIONS_WITH_MISSING_DIGIT = [
    "57020-56",
    "5702056",
    "57020 56",
    "57020.56",
    "57020/56",
    "57020_56",
    "57020-56 ",
    " 57020-56",
    " 57020-56 ",
    "57020 - 56",
    "57020- 56",
    "57020 -56",
    "57.020-56",
    "57 020 56",
    "57-020-56",
    "57/020/56",
]

INVALID_LENGTH_CEPS = (
    INVALID_CEP_VARIATIONS_WITH_EXTRA_DIGIT + INVALID_CEP_VARIATIONS_WITH_MISSING_DIGIT
)


@pytest.mark.parametrize("cep_input", VALID_CEP_VARIATIONS)
def test_validate_cep_accepts_supported_formats(cep_input: str):
    assert validate_cep(cep_input) == "57020565"


@pytest.mark.parametrize("cep_input", VALID_CEP_VARIATIONS)
def test_cep_field_normalizes_to_digits(cep_input: str):
    model = _CEPModel(cep=cep_input)
    assert model.cep == "57020565"


@pytest.mark.parametrize("cep_input", INVALID_LENGTH_CEPS)
def test_cep_field_rejects_invalid_lengths(cep_input: str):
    with pytest.raises(ValidationError):
        _CEPModel(cep=cep_input)


def test_cep_canonical_eight_digits_round_trip_display_format():
    """Digits normalize to 8 chars; common display form is NNNNN-NNN."""
    digits = validate_cep("57020-565")
    assert digits == "57020565"
    assert f"{digits[:5]}-{digits[5:]}" == "57020-565"
