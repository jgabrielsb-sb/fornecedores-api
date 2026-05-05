from datetime import UTC, datetime

import pytest

from fornecedores_app.api.v1.models import FornecedorCreate, FornecedorOnProtheusVersion0Create
from fornecedores_app.api.v1.models.dto_fornecedor_on_protheus import FornecedorOnProtheusUpdate
from fornecedores_app.api.v1.repos import fornecedor_on_protheus_repo, fornecedor_repo
from fornecedores_app.db.schemas import FornecedorOnProteusSchema


@pytest.fixture
def fornecedor_id(db_session) -> int:
    now = datetime.now(UTC)
    parent = fornecedor_repo.create(
        FornecedorCreate(cnpj="11111111111111"),
        now=now,
        session=db_session,
    )
    db_session.flush()
    return parent.id

@pytest.fixture
def fornecedor_on_protheus_to_update() -> FornecedorOnProtheusUpdate:
    return FornecedorOnProtheusUpdate(
        cep='31310240'
    )


class TestCreateFornecedorOnProtheus:
    def test_should_create_fornecedor_on_protheus_with_valid_data(
        self,
        db_session,
        fornecedor_id: int,
    ):
        now = datetime.now(UTC)
        dto = FornecedorOnProtheusVersion0Create(
            id_fornecedor=fornecedor_id,
        )
        row = fornecedor_on_protheus_repo.create_version_0(
            dto,
            now=now,
            session=db_session,
        )

        assert isinstance(row, FornecedorOnProteusSchema)
        assert row.id_fornecedor == fornecedor_id
        assert row.created_at == now
        assert row.updated_at == now
        assert row.cep is None
        assert row.version == 0
        assert row.to_update is False
        assert row.protheus_synced_version == 0
        assert row.id is not None


class TestGetFornecedorOnProtheusById:
    def test_should_return_the_row_given_existent_id(
        self,
        db_session,
        fornecedor_id: int,
    ):
        now = datetime.now(UTC)
        dto = FornecedorOnProtheusVersion0Create(
            id_fornecedor=fornecedor_id,
        )
        created = fornecedor_on_protheus_repo.create_version_0(
            dto,
            now=now,
            session=db_session,
        )

        found = fornecedor_on_protheus_repo.get_fornecedor_on_protheus_by_id(
            created.id,
            db_session,
        )

        assert found is not None
        assert found.id == created.id
        assert found.id_fornecedor == fornecedor_id
        assert found.created_at == now
        assert found.updated_at == now

    def test_should_return_none_given_non_existent_id(self, db_session):
        assert (
            fornecedor_on_protheus_repo.get_fornecedor_on_protheus_by_id(
                424242,
                db_session,
            )
            is None
        )

class TestUpdateFornecedorOnProtheus:
    def test_should_increment_version_when_update_is_called(
        self,
        fornecedor_id: int,
        fornecedor_on_protheus_to_update: FornecedorOnProtheusUpdate,
        db_session
    ):
        row = fornecedor_on_protheus_repo.get_fornecedor_on_protheus_by_fornecedor_id(
            fornecedor_id,
            db_session
        )

        assert row.version == 0
        assert row.cep is None
        
        now = datetime.now(UTC)
        row_after_update = fornecedor_on_protheus_repo.update_fornecedor_on_protheus(
            id=row.id,
            fornecedor_on_protheus=fornecedor_on_protheus_to_update,
            now=now,
            session=db_session
        )

        assert row_after_update.version == 1
        assert row_after_update.updated_at == now
        assert row_after_update.cep == fornecedor_on_protheus_to_update.cep

class TestSyncProtheusSyncedVersion:
    def test_should_sync_protheus_synced_version_when_sync_is_called(
        self,
        fornecedor_id: int,
        fornecedor_on_protheus_to_update: FornecedorOnProtheusUpdate,
        db_session
    ):
        row = fornecedor_on_protheus_repo.get_fornecedor_on_protheus_by_fornecedor_id(
            fornecedor_id,
            db_session
        )
        assert row.version == 0
        assert row.protheus_synced_version == 0
        assert row.protheus_last_synced_at is None

        now_update = datetime.now(UTC)
        row_after_update = fornecedor_on_protheus_repo.update_fornecedor_on_protheus(
            id=row.id,
            fornecedor_on_protheus=fornecedor_on_protheus_to_update,
            now=now_update,
            session=db_session
        )
        
        assert row_after_update.version == 1
        assert row_after_update.updated_at == now_update
        assert row_after_update.cep == fornecedor_on_protheus_to_update.cep

        # assert that protheus column remains the same
        assert row_after_update.protheus_synced_version == 0
        assert row_after_update.protheus_last_synced_at is None

        now_sync = datetime.now(UTC)
        row_after_sync = fornecedor_on_protheus_repo.sync_protheus_synced_version(
            id=row.id,
            now=now_sync,
            session=db_session
        )

        assert row_after_sync.protheus_synced_version == 1
        assert row_after_sync.protheus_last_synced_at == now_sync

        # assert that updated_at remains the same
        assert row_after_sync.updated_at == now_update


class TestSetToUpdateToTrue:
    def test_should_set_to_update_to_true_when_set_to_update_to_true_is_called(
        self,
        fornecedor_id: int,
        db_session
    ):
        row = fornecedor_on_protheus_repo.get_fornecedor_on_protheus_by_fornecedor_id(
            fornecedor_id,
            db_session
        )
        assert row.to_update is False
        
        row_after_set_to_update_to_true = fornecedor_on_protheus_repo.set_to_update_to_true(
            id=row.id,
            session=db_session
        )
        assert row_after_set_to_update_to_true.to_update is True

class TestSetToUpdateToFalse:
    def test_should_set_to_update_to_false_when_set_to_update_to_false_is_called(
        self,
        fornecedor_id: int,
        db_session
    ):
        row = fornecedor_on_protheus_repo.get_fornecedor_on_protheus_by_fornecedor_id(
            fornecedor_id,
            db_session
        )
         
        fornecedor_on_protheus_repo.set_to_update_to_true(
            id=row.id,
            session=db_session
        )
        assert row.to_update is True

        row_after_set_to_update_to_false = fornecedor_on_protheus_repo.set_to_update_to_false(
            id=row.id,
            session=db_session
        )
        
        assert row_after_set_to_update_to_false.to_update is False
       