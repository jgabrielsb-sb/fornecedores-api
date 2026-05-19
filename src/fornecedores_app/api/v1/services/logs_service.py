from datetime import UTC, datetime

from sqlalchemy.orm import Session

from fornecedores_app.api.v1.models import dto_logs, dto_responses
from fornecedores_app.api.v1.repos import logs_repo
from fornecedores_app.api.v1.services.exceptions import NotFoundException


def create_log(
    log_create: dto_logs.LogCreate,
    session: Session,
) -> dto_logs.LogResponse:
    now = datetime.now(UTC)
    db_log = logs_repo.create(log_create, now=now, session=session)
    log_response = dto_logs.LogResponse.model_validate(db_log)
    session.commit()
    return log_response


def get_logs(
    log_filter: dto_logs.LogFilter,
    session: Session,
) -> dto_responses.PaginatedResponse[dto_logs.LogResponse]:
    logs_db, total_items = logs_repo.get(log_filter, session)
    logs_response = [dto_logs.LogResponse.model_validate(log) for log in logs_db]

    total_pages = max(1, (total_items + log_filter.limit - 1) // log_filter.limit)
    meta = dto_responses.PageMeta(
        page=log_filter.page,
        per_page=log_filter.limit,
        total_items=total_items,
        total_pages=total_pages,
        has_next=log_filter.page < total_pages,
        has_previous=log_filter.page > 1,
    )

    return dto_responses.PaginatedResponse(data=logs_response, meta=meta)


def get_log_by_id(
    log_id: int,
    session: Session,
) -> dto_logs.LogResponse:
    db_log = logs_repo.get_by_id(log_id, session)

    if not db_log:
        raise NotFoundException(
            resource="id",
            identifier=str(log_id),
            object="log",
        )

    return dto_logs.LogResponse.model_validate(db_log)
