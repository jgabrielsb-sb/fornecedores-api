from datetime import UTC, datetime

import pytest

from fornecedores_app.api.v1.models import FornecedorCreate

pytestmark = pytest.mark.unit
from fornecedores_app.api.v1.repos import fornecedor_repo, fornecedor_on_protheus_repo
from fornecedores_app.db.schemas import FornecedoresSchema


@pytest.fixture
def fornecedor_create() -> FornecedorCreate:
    return FornecedorCreate(
        cnpj="12345678912345",
    )


class TestCreateFornecedor:
    def test_should_create_fornecedor_with_valid_data(
        self,
        db_session,
        fornecedor_create: FornecedorCreate,
    ):
        now = datetime.now(UTC)
        fornecedor_returned = fornecedor_repo.create(
            fornecedor_create,
            now=now,
            session=db_session,
        )

        assert isinstance(fornecedor_returned, FornecedoresSchema)
        assert fornecedor_returned.cnpj == fornecedor_create.cnpj
        assert fornecedor_returned.updated_at == now
        assert fornecedor_returned.created_at == now
        assert fornecedor_returned is not None
    
    def test_should_create_fornecedor_on_protheus_with_valid_data(
        self,
        db_session,
        fornecedor_create: FornecedorCreate,
    ):
        now = datetime.now(UTC)
        fornecedor_returned = fornecedor_repo.create(
            fornecedor_create,
            now=now,
            session=db_session,
        )
        
        assert isinstance(fornecedor_returned, FornecedoresSchema)
        assert fornecedor_returned.cnpj == fornecedor_create.cnpj
        assert fornecedor_returned.updated_at == now
        assert fornecedor_returned.created_at == now
        assert fornecedor_returned is not None
        
        fornecedor_on_protheus_returned = fornecedor_on_protheus_repo.get_fornecedor_on_protheus_by_id(fornecedor_returned.id, session=db_session)
        assert fornecedor_on_protheus_returned is not None
        assert fornecedor_on_protheus_returned.id_fornecedor == fornecedor_returned.id

class TestGetFornecedorByCNPJ:
    def test_should_return_the_fornecedor_given_existent_cnpj(
        self, db_session, fornecedor_create: FornecedorCreate
    ):
        now = datetime.now(UTC)
        created = fornecedor_repo.create(fornecedor_create, now=now, session=db_session)

        found = fornecedor_repo.get_fornecedor_by_cnpj(fornecedor_create.cnpj, db_session)

        assert found is not None
        assert found.id == created.id
        assert found.cnpj == fornecedor_create.cnpj
        assert found.created_at == now
        assert found.updated_at == now

    def test_should_return_none_given_non_existent_cnpj(self, db_session, fornecedor_create: FornecedorCreate):
        assert fornecedor_repo.get_fornecedor_by_cnpj(fornecedor_create.cnpj, db_session) is None


class TestGetFornecedorByID:
    def test_should_return_the_fornecedor_given_existent_id(self, db_session, fornecedor_create: FornecedorCreate):
        now = datetime.now(UTC)
        created = fornecedor_repo.create(fornecedor_create, now=now, session=db_session)

        found = fornecedor_repo.get_by_id(created.id, session=db_session)

        assert found is not None
        assert found.id == created.id
        assert found.cnpj == fornecedor_create.cnpj
        assert found.created_at == now
        assert found.updated_at == now

    def test_should_return_none_given_non_existent_id(self, db_session, fornecedor_create: FornecedorCreate):
        assert fornecedor_repo.get_by_id(424242, session=db_session) is None
