from typing import (
    Any,
    Generator,
)

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    Session,
    sessionmaker,
)

from fornecedores_app.core.config import settings
from fornecedores_app.db.schemas.schemas import Base

engine = create_engine(
    settings.DB_URL_WITH_LIBRARY,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_db() -> None:
    Base.metadata.create_all(engine)


def get_db() -> Generator[Session, Any, None]:
    with session_maker() as session:
        try:
            yield session
        finally:
            session.close()
