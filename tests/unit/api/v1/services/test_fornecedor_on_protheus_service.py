from datetime import UTC, datetime
from itertools import count

import pytest

from fornecedores_app.api.v1.models import (
    FornecedorCreate,
    FornecedorOnProtheusResponse,
    FornecedorOnProtheusUpdate,
)
from fornecedores_app.api.v1.repos import fornecedor_on_protheus_repo, fornecedor_repo
from fornecedores_app.api.v1.services import fornecedor_on_protheus_service
from fornecedores_app.api.v1.services.exceptions import (
    ForbiddenException,
    NotFoundException,
)

pytestmark = pytest.mark.unit

_cnpj_counter = count(1)


@pytest.fixture
def fornecedor_on_protheus(db_session):
    now = datetime.now(UTC)
    cnpj = f"{next(_cnpj_counter):014d}"
    fornecedor = fornecedor_repo.create(
        FornecedorCreate(cnpj=cnpj),
        now=now,
        session=db_session,
    )
    return fornecedor_on_protheus_repo.get_fornecedor_on_protheus_by_fornecedor_id(
        fornecedor.id,
        db_session,
    )


@pytest.fixture
def fornecedor_on_protheus_to_update() -> FornecedorOnProtheusUpdate:
    return FornecedorOnProtheusUpdate(cep="57020-565")


class TestUpdateFornecedorOnProtheus:
    def test_should_raise_not_found_exception_if_fornecedor_on_protheus_does_not_exist(
        self,
        db_session,
        fornecedor_on_protheus_to_update: FornecedorOnProtheusUpdate,
    ):
        with pytest.raises(NotFoundException):
            fornecedor_on_protheus_service.update(
                id=424242,
                fornecedor_on_protheus=fornecedor_on_protheus_to_update,
                now=datetime.now(UTC),
                session=db_session,
            )

    def test_should_raise_forbidden_exception_if_to_update_is_false(
        self,
        db_session,
        fornecedor_on_protheus,
        fornecedor_on_protheus_to_update: FornecedorOnProtheusUpdate,
    ):
        assert fornecedor_on_protheus.to_update is False

        with pytest.raises(ForbiddenException):
            fornecedor_on_protheus_service.update(
                id=fornecedor_on_protheus.id,
                fornecedor_on_protheus=fornecedor_on_protheus_to_update,
                now=datetime.now(UTC),
                session=db_session,
            )

    def test_should_update_fornecedor_on_protheus(
        self,
        db_session,
        fornecedor_on_protheus,
        fornecedor_on_protheus_to_update: FornecedorOnProtheusUpdate,
    ):
        fornecedor_on_protheus_repo.set_to_update_to_true(
            id=fornecedor_on_protheus.id,
            session=db_session,
        )
        now = datetime.now(UTC)

        result = fornecedor_on_protheus_service.update(
            id=fornecedor_on_protheus.id,
            fornecedor_on_protheus=fornecedor_on_protheus_to_update,
            now=now,
            session=db_session,
        )

        assert result.id == fornecedor_on_protheus.id
        assert result.cep == fornecedor_on_protheus_to_update.cep
        assert result.version == 1
        assert result.updated_at.replace(tzinfo=UTC) == now

    def test_should_set_to_update_to_false_after_update(
        self,
        db_session,
        fornecedor_on_protheus,
        fornecedor_on_protheus_to_update: FornecedorOnProtheusUpdate,
    ):
        fornecedor_on_protheus_repo.set_to_update_to_true(
            id=fornecedor_on_protheus.id,
            session=db_session,
        )

        fornecedor_on_protheus_service.update(
            id=fornecedor_on_protheus.id,
            fornecedor_on_protheus=fornecedor_on_protheus_to_update,
            now=datetime.now(UTC),
            session=db_session,
        )

        row = fornecedor_on_protheus_repo.get_fornecedor_on_protheus_by_id(
            fornecedor_on_protheus.id,
            db_session,
        )
        assert row.to_update is False

    def test_should_return_protheus_response(
        self,
        db_session,
        fornecedor_on_protheus,
        fornecedor_on_protheus_to_update: FornecedorOnProtheusUpdate,
    ):
        fornecedor_on_protheus_repo.set_to_update_to_true(
            id=fornecedor_on_protheus.id,
            session=db_session,
        )

        result = fornecedor_on_protheus_service.update(
            id=fornecedor_on_protheus.id,
            fornecedor_on_protheus=fornecedor_on_protheus_to_update,
            now=datetime.now(UTC),
            session=db_session,
        )

        assert isinstance(result, FornecedorOnProtheusResponse)
        assert result.id == fornecedor_on_protheus.id
        assert result.id_fornecedor == fornecedor_on_protheus.id_fornecedor
        assert result.protheus_synced_version == 0
        assert result.protheus_last_synced_at is None


class TestSyncProtheusSyncedVersion:
    def test_should_raise_not_found_exception_if_fornecedor_on_protheus_does_not_exist(
        self,
        db_session,
    ):
        with pytest.raises(NotFoundException):
            fornecedor_on_protheus_service.sync_protheus_synced_version(
                id=424242,
                now=datetime.now(UTC),
                session=db_session,
            )

    def test_should_update_protheus_last_synced_at_and_synced_version_when_not_yet_synced(
        self,
        db_session,
        fornecedor_on_protheus,
        fornecedor_on_protheus_to_update: FornecedorOnProtheusUpdate,
    ):
        fornecedor_on_protheus_repo.update_fornecedor_on_protheus(
            id=fornecedor_on_protheus.id,
            fornecedor_on_protheus=fornecedor_on_protheus_to_update,
            now=datetime.now(UTC),
            session=db_session,
        )

        now_sync = datetime.now(UTC)
        result = fornecedor_on_protheus_service.sync_protheus_synced_version(
            id=fornecedor_on_protheus.id,
            now=now_sync,
            session=db_session,
        )

        assert result.protheus_last_synced_at.replace(tzinfo=UTC) == now_sync
        assert result.protheus_synced_version == result.version

    def test_should_not_update_protheus_last_synced_at_when_already_synced(
        self,
        db_session,
        fornecedor_on_protheus,
        fornecedor_on_protheus_to_update: FornecedorOnProtheusUpdate,
    ):
        fornecedor_on_protheus_repo.update_fornecedor_on_protheus(
            id=fornecedor_on_protheus.id,
            fornecedor_on_protheus=fornecedor_on_protheus_to_update,
            now=datetime.now(UTC),
            session=db_session,
        )

        now_first_sync = datetime.now(UTC)
        fornecedor_on_protheus_service.sync_protheus_synced_version(
            id=fornecedor_on_protheus.id,
            now=now_first_sync,
            session=db_session,
        )

        now_second_sync = datetime.now(UTC)
        result = fornecedor_on_protheus_service.sync_protheus_synced_version(
            id=fornecedor_on_protheus.id,
            now=now_second_sync,
            session=db_session,
        )

        assert result.protheus_last_synced_at.replace(tzinfo=UTC) == now_first_sync
        assert result.protheus_synced_version == result.version


class TestSetToUpdateToTrue:
    def test_should_raise_not_found_exception_if_fornecedor_on_protheus_does_not_exist(
        self,
        db_session,
    ):
        with pytest.raises(NotFoundException):
            fornecedor_on_protheus_service.set_to_update_to_true(
                id=424242,
                session=db_session,
            )

    def test_should_set_to_update_to_true(
        self,
        db_session,
        fornecedor_on_protheus,
    ):
        assert fornecedor_on_protheus.to_update is False

        result = fornecedor_on_protheus_service.set_to_update_to_true(
            id=fornecedor_on_protheus.id,
            session=db_session,
        )

        assert isinstance(result, FornecedorOnProtheusResponse)
        assert result.to_update is True
