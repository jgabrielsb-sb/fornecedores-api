from datetime import datetime
from typing import List, Tuple

from sqlalchemy import String, cast, or_
from sqlalchemy.orm import Session

from fornecedores_app.api.v1.models import dto_logs
from fornecedores_app.db.schemas.schemas import LogSchema


def _metadata_json_compare_variants(value: str) -> tuple[str, ...]:
    """
    SQLite JSON_EXTRACT casts booleans to '1'/'0'; PostgreSQL ->> uses 'true'/'false'.
    OR these so filtering with "true"/"false" matches stored JSON booleans on both.
    """
    variants = [value]
    low = value.lower()
    if low == "true":
        variants.extend(["true", "1", "True"])
    elif low == "false":
        variants.extend(["false", "0", "False"])
    seen: set[str] = set()
    uniq: list[str] = []
    for v in variants:
        if v not in seen:
            seen.add(v)
            uniq.append(v)
    return tuple(uniq)


def _filter_metadata_json_key_equals(query, key: str, value: str):
    meta_expr = cast(LogSchema.metadata_json[key].as_string(), String)
    variants = _metadata_json_compare_variants(value)
    if len(variants) == 1:
        return query.filter(meta_expr == variants[0])
    return query.filter(or_(*[meta_expr == v for v in variants]))


def create(
    log: dto_logs.LogCreate,
    *,
    now: datetime,
    session: Session,
) -> LogSchema:
    db_log = LogSchema(
        **log.model_dump(),
        created_at=now,
        updated_at=now,
    )
    session.add(db_log)
    session.flush()
    return db_log


def get(
    log_filter: dto_logs.LogFilter,
    session: Session,
) -> Tuple[List[LogSchema], int]:
    query = session.query(LogSchema)

    if log_filter.start_date is not None:
        query = query.filter(LogSchema.execution_time >= log_filter.start_date)

    if log_filter.end_date is not None:
        query = query.filter(LogSchema.execution_time <= log_filter.end_date)

    if log_filter.process_name is not None:
        query = query.filter(LogSchema.process_name.ilike(f"%{log_filter.process_name}%"))

    if log_filter.status is not None:
        query = query.filter(LogSchema.status == log_filter.status)

    if log_filter.trace_id is not None:
        query = query.filter(LogSchema.trace_id == log_filter.trace_id)

    if log_filter.metadata_key is not None and log_filter.metadata_value is not None:
        query = _filter_metadata_json_key_equals(
            query, log_filter.metadata_key, log_filter.metadata_value
        )

    if log_filter.parsed_metadata_match:
        for mk, mv in log_filter.parsed_metadata_match.items():
            query = _filter_metadata_json_key_equals(query, mk, mv)

    total_items = query.count()
    offset = (log_filter.page - 1) * log_filter.limit
    query = query.offset(offset).limit(log_filter.limit)
    return query.all(), total_items


def get_by_id(
    log_id: int,
    session: Session,
) -> LogSchema | None:
    return session.query(LogSchema).filter(LogSchema.id == log_id).first()
