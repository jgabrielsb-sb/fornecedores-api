from typing import Annotated, Any
import re

from pydantic import AfterValidator, WithJsonSchema


def validate_cnpj(value: str) -> str:
    digits = re.sub(r"\D", "", str(value))
    if len(digits) != 14:
        raise ValueError(f"CNPJ length must be 14 digits, but got {len(digits)}")
    return digits


CNPJField = Annotated[
    str,
    AfterValidator(validate_cnpj),
    WithJsonSchema(
        {
            "type": "string",
            "title": "CNPJ",
            "description": "Brazilian CNPJ. Accepts digits or formatted value.",
            "examples": ["12345678000195", "12.345.678/0001-95"],
            "pattern": r"^\d{2}\.?\d{3}\.?\d{3}/?\d{4}-?\d{2}$",
        }
    ),
]