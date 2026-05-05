import re
from typing import Annotated, Any

from pydantic import AfterValidator, WithJsonSchema


def validate_cep(value: Any) -> str:
    digits = re.sub(r"\D", "", str(value))
    if len(digits) != 8:
        raise ValueError(f"CEP length must be 8 digits, but got {len(digits)}")
    return digits


CEPField = Annotated[
    str,
    AfterValidator(validate_cep),
    WithJsonSchema(
        {
            "type": "string",
            "title": "CEP",
            "description": "Brazilian CEP. Accepts digits or formatted value.",
            "examples": ["31310240", "31310-240"],
            "pattern": r"^\d{5}-?\d{3}$",
        }
    ),
]
