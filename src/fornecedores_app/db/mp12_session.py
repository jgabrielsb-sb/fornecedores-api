from typing import Any, Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from fornecedores_app.config import settings

engine = create_engine(
    settings.MP12_DB_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

session_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, Any, None]:
    with session_maker() as session:
        try:
            yield session
        finally:
            session.close()
