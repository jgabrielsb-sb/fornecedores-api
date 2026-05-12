import re
from typing import Annotated

from pydantic import AfterValidator, WithJsonSchema


def validate_codigo_ibge(value: str) -> str:
    digits = re.sub(r"\D", "", str(value))
    if len(digits) != 7:
        raise ValueError(f"Codigo IBGE length must be 7 digits, but got {len(digits)}")
    return digits


CodigoIBGEField = Annotated[
    str,
    AfterValidator(validate_codigo_ibge),
    WithJsonSchema(
        {
            "type": "string",
            "title": "Codigo IBGE",
            "description": "Brazilian IBGE municipality code. Accepts digits or formatted value.",
            "examples": ["1200013", "2701605"],
            "pattern": r"^\d{7}$",
        }
    ),
]
