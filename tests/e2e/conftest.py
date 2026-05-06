import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

from fornecedores_app.api.main import create_app
from fornecedores_app.config.config import settings
from fornecedores_app.db.schemas.schemas import Base
from fornecedores_app.db.session import get_db


def _ensure_test_environment():
    if settings.APP_ENV != "test":
        raise ValueError(
            f"APP_ENV must be set to 'test' (got '{settings.APP_ENV}')"
        )
    if "test" not in settings.DB_NAME:
        raise ValueError(
            "Refusing to run E2E tests: DB_NAME must contain 'test' "
            f"(got '{settings.DB_NAME}')"
        )


_ensure_test_environment()

test_engine = create_engine(
    settings.DB_URL_WITH_LIBRARY,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)


@pytest.fixture(scope="session")
def setup_database():
    Base.metadata.create_all(test_engine)
    yield
    Base.metadata.drop_all(test_engine)


@pytest.fixture
def db_session(setup_database):
    connection = test_engine.connect()
    trans = connection.begin()
    SessionLocal = sessionmaker(bind=connection, autoflush=False, autocommit=False)
    session = SessionLocal()
    session.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def _restart_savepoint(_sess, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.begin_nested()

    try:
        yield session
    finally:
        session.close()
        trans.rollback()
        connection.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app = create_app()
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()
