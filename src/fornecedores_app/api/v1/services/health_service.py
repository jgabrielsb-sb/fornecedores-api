from sqlalchemy.orm import Session

from fornecedores_app.api.v1.models.dto_health import HealthResponse
from fornecedores_app.api.v1.repos import health_repo


def get_health(session: Session) -> HealthResponse:
    health_repo.ping_database(session)
    return HealthResponse(status="ok", database="connected")
