# tests/conftest.py
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from fornecedores_app.db.schemas.schemas import Base  # where all models' metadata live

@pytest.fixture(scope="session")
def engine():
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)

@pytest.fixture
def db_session(engine):
    """
    Use a SAVEPOINT per test so data is rolled back quickly.
    """
    connection = engine.connect()
    trans = connection.begin()
    SessionLocal = sessionmaker(bind=connection, autoflush=False, autocommit=False)
    session = SessionLocal()

    # Support nested transactions for tests that call session.begin()
    session.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def _restart_savepoint(sess, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.begin_nested()

    try:
        yield session
    finally:
        session.close()
        trans.rollback()
        connection.close()
