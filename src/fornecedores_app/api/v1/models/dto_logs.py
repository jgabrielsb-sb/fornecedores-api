import json
import re

from pydantic import (
    BaseModel,
    BeforeValidator,
    ConfigDict,
    Field,
    PrivateAttr,
    model_validator,
)

from typing import Annotated, Any, Optional
from datetime import datetime

_METADATA_KEY_RE = re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*$")


def _parse_metadata_match_json(v: str | None) -> dict[str, str] | None:
    if v is None or v == "":
        return None
    raw = json.loads(v)
    if not isinstance(raw, dict):
        raise ValueError("metadata_match must be a JSON object")
    if len(raw) == 0:
        return None
    out: dict[str, str] = {}
    for key, val in raw.items():
        ks = str(key)
        if not _METADATA_KEY_RE.match(ks):
            raise ValueError(f"Invalid metadata key: {ks!r}")
        if isinstance(val, bool):
            out[ks] = "true" if val else "false"
        elif val is None:
            raise ValueError("metadata_match values cannot be null")
        else:
            out[ks] = str(val)
    return out


def _metadata_match_query_input(v: Any) -> str | None:
    """Accept JSON text (HTTP query) or dict (tests); OpenAPI type stays str so Swagger shows a query param."""
    if v is None or v == "":
        return None
    if isinstance(v, dict):
        return json.dumps(v, separators=(",", ":"))
    if isinstance(v, str):
        s = v.strip()
        return s if s else None
    raise TypeError("metadata_match must be a string or object")


class LogCreate(BaseModel):
    trace_id: str
    execution_time: datetime
    message: str
    process_name: str
    status: str
    metadata_json: Optional[dict[str, Any]] = None


class LogResponse(LogCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class LogFilter(BaseModel):
    start_date: Optional[datetime] = Field(
        None,
        description="Filter logs with execution_time >= this value (ISO 8601).",
    )
    end_date: Optional[datetime] = Field(
        None,
        description="Filter logs with execution_time <= this value (ISO 8601).",
    )
    process_name: Optional[str] = Field(
        None,
        description="Filter logs by process_name (case-insensitive contains match).",
    )
    status: Optional[str] = Field(
        None,
        description="Filter logs by status (exact match).",
    )
    trace_id: Optional[str] = Field(
        None,
        description="Filter logs by trace_id (exact match).",
    )

    metadata_key: Optional[str] = Field(
        None,
        description=(
            "Top-level key inside metadata_json to match (use with metadata_value). "
            "Only letters, digits, and underscore; must start with a letter or underscore."
        ),
        pattern=r"^[a-zA-Z_][a-zA-Z0-9_]*$",
    )
    metadata_value: Optional[str] = Field(
        None,
        description=(
            "String value to match for metadata_key inside metadata_json "
            "(compared as text, same as JSON ->> in PostgreSQL)."
        ),
    )
    metadata_match: Annotated[
        str | None,
        BeforeValidator(_metadata_match_query_input),
    ] = Field(
        default=None,
        description=(
            "JSON object as a single string: top-level keys map to string values; all must match (AND). "
            'Example: {"invoice_id":"234","batch":"a"}. URL-encode in the query string. '
            "Can be combined with metadata_key and metadata_value."
        ),
        examples=['{"invoice_id":"234","batch":"a"}'],
    )

    page: Optional[int] = Field(
        1,
        ge=1,
        description="Page number for pagination (starts at 1)",
    )
    limit: Optional[int] = Field(
        10,
        ge=1,
        le=100,
        description="Number of items per page (max 100)",
    )

    _metadata_match_parsed: dict[str, str] | None = PrivateAttr(default=None)

    @property
    def parsed_metadata_match(self) -> dict[str, str] | None:
        return self._metadata_match_parsed

    @model_validator(mode="after")
    def _finalize_metadata_filters(self) -> "LogFilter":
        if (self.metadata_key is None) != (self.metadata_value is None):
            raise ValueError(
                "metadata_key and metadata_value must both be provided or both omitted"
            )
        self._metadata_match_parsed = _parse_metadata_match_json(self.metadata_match)
        return self
