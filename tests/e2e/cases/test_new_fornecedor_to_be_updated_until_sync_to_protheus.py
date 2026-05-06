import pytest
from datetime import UTC, datetime

from fornecedores_app.api.v1.models import FornecedorResponse
from fornecedores_app.api.v1.models.dto_fornecedor_on_protheus import FornecedorOnProtheusResponse
from fornecedores_app.api.v1.repos import fornecedor_on_protheus_repo

from tests.e2e.helpers.assert_fornedor_on_protheus_created_at import assert_fornedor_on_protheus_created_at
from tests.e2e.helpers.assert_fornecedor_on_protheus_updated_at import assert_fornecedor_on_protheus_updated_at
from tests.e2e.helpers.assert_fornecedor_on_protheus_last_synced_at import assert_fornecedor_on_protheus_last_synced_at
from tests.e2e.helpers.assert_fornecedor_on_protheus_version import assert_fornecedor_on_protheus_version
from tests.e2e.helpers.assert_fornecedor_protheus_synced_version import assert_fornecedor_protheus_synced_version

pytestmark = pytest.mark.e2e


class TestNewFornecedorWorkflowUntilSyncToProtheus:
    def test_correct_workflow_to_update_new_fornecedor(self, client, db_session):
        """
        Workflow:
            * POST /api/v1/fornecedores/ com fornecedor válido
                OBS: guardar t_before_create / t_after_create como janela de tempo da criação;
                - Verificar resposta:
                    # status 201
                    # contém um modelo válido de FornecedorResponse

                - Verificar se fornecedor_on_protheus foi criado na tabela com os dados:
                    # created_at dentro da janela de tempo de criação
                    # updated_at dentro da janela de tempo de criação
                    # version = 0, protheus_synced_version = 0, to_update = False, protheus_last_synced_at = None

            * POST /api/v1/fornecedores-on-protheus/{id}/mark-for-update
                - Verificar resposta:
                    # status 200
                    # contém um modelo válido de FornecedorOnProtheusResponse

                - Verificar se o fornecedor no protheus está com o campo to_update = True
                - Verificar se updated_at ficou inalterado (ainda dentro da janela de criação)

            * PATCH /api/v1/fornecedores-on-protheus/{id}
                OBS: guardar t_before_update / t_after_update como janela de tempo do update;
                - Verificar resposta:
                    # status 200
                    # contém um modelo válido de FornecedorOnProtheusResponse

                - Verificar se o fornecedor no protheus:
                    # tem o campo version incrementado para 1
                    # tem o campo updated_at dentro da janela de tempo de atualização
                    # to_update é False

            * POST /api/v1/fornecedores-on-protheus/{id}/sync
                OBS: guardar t_before_sync / t_after_sync como janela de tempo da sincronização;
                - Verificar resposta:
                    # status 200
                    # contém um modelo válido de FornecedorOnProtheusResponse

                - Verificar se protheus_last_synced_at está dentro da janela de sincronização
                - Verificar se protheus_synced_version == version (== 1)

            No final do processo, verificar o estado consolidado do registro:
                # created_at dentro da janela de criação
                # updated_at dentro da janela de atualização (não da criação)
                # protheus_last_synced_at dentro da janela de sincronização
        """
        # ── Step 1: create fornecedor ───────────────────────────────────────
        t_before_create = datetime.now(UTC)
        response = client.post("/api/v1/fornecedores/", json={"cnpj": "62173620000180"})
        t_after_create = datetime.now(UTC)

        assert response.status_code == 201
        FornecedorResponse.model_validate(response.json())
        fornecedor_id = response.json()["id"]

        fop = fornecedor_on_protheus_repo.get_fornecedor_on_protheus_by_fornecedor_id(
            fornecedor_id, db_session
        )
        assert fop is not None
        assert_fornedor_on_protheus_created_at(fop, t_before_create, t_after_create)
        assert_fornecedor_on_protheus_updated_at(fop, t_before_create, t_after_create)
        assert fop.version == 0
        assert fop.protheus_synced_version == 0
        assert fop.to_update is False
        assert fop.protheus_last_synced_at is None

        fop_id = fop.id

        # ── Step 2: mark for update ─────────────────────────────────────────
        response = client.post(f"/api/v1/fornecedores-on-protheus/{fop_id}/mark-for-update")

        assert response.status_code == 200
        FornecedorOnProtheusResponse.model_validate(response.json())

        fop = fornecedor_on_protheus_repo.get_fornecedor_on_protheus_by_id(fop_id, db_session)
        assert fop.to_update is True
        assert_fornecedor_on_protheus_updated_at(fop, t_before_create, t_after_create)

        # ── Step 3: patch update ────────────────────────────────────────────
        t_before_update = datetime.now(UTC)
        response = client.patch(
            f"/api/v1/fornecedores-on-protheus/{fop_id}",
            json={"cep": "57020-565"},
        )
        t_after_update = datetime.now(UTC)

        assert response.status_code == 200
        FornecedorOnProtheusResponse.model_validate(response.json())

        fop = fornecedor_on_protheus_repo.get_fornecedor_on_protheus_by_id(fop_id, db_session)
        assert_fornecedor_on_protheus_version(fop, 1)
        assert_fornecedor_on_protheus_updated_at(fop, t_before_update, t_after_update)
        assert fop.to_update is False

        # ── Step 4: sync ────────────────────────────────────────────────────
        t_before_sync = datetime.now(UTC)
        response = client.post(f"/api/v1/fornecedores-on-protheus/{fop_id}/sync")
        t_after_sync = datetime.now(UTC)

        assert response.status_code == 200
        FornecedorOnProtheusResponse.model_validate(response.json())

        fop = fornecedor_on_protheus_repo.get_fornecedor_on_protheus_by_id(fop_id, db_session)
        assert_fornecedor_on_protheus_last_synced_at(fop, t_before_sync, t_after_sync)
        assert_fornecedor_protheus_synced_version(fop, 1)

        # ── Final consolidated state ────────────────────────────────────────
        assert_fornedor_on_protheus_created_at(fop, t_before_create, t_after_create)
        assert_fornecedor_on_protheus_updated_at(fop, t_before_update, t_after_update)
        assert_fornecedor_on_protheus_last_synced_at(fop, t_before_sync, t_after_sync)

    
    def test_incorrect_workflow_to_update_new_fornecedor(self, client, db_session):
        """
        Testa o caminho de erro: PATCH é tentado antes de mark-for-update (to_update = False).
        O sistema deve rejeitar o update com 403, manter o estado do registro intacto,
        e permitir completar o fluxo corretamente após o mark-for-update.

        Workflow:
            * POST /api/v1/fornecedores/ com fornecedor válido
                OBS: guardar t_before_create / t_after_create como janela de tempo da criação;
                - Verificar resposta:
                    # status 201
                    # contém um modelo válido de FornecedorResponse

                - Verificar se fornecedor_on_protheus foi criado na tabela com os dados:
                    # created_at dentro da janela de tempo de criação
                    # updated_at dentro da janela de tempo de criação
                    # version = 0, protheus_synced_version = 0, to_update = False, protheus_last_synced_at = None

            * PATCH /api/v1/fornecedores-on-protheus/{id}  (sem mark-for-update antes)
                - Verificar resposta:
                    # status 403
                - Verificar que o estado do registro no banco não foi alterado:
                    # version ainda 0, to_update ainda False, updated_at inalterado

            * POST /api/v1/fornecedores-on-protheus/{id}/mark-for-update
                - Verificar resposta:
                    # status 200
                    # contém um modelo válido de FornecedorOnProtheusResponse
                - Verificar se o fornecedor no protheus está com o campo to_update = True
                - Verificar se updated_at ficou inalterado (ainda dentro da janela de criação)

            * PATCH /api/v1/fornecedores-on-protheus/{id}
                OBS: guardar t_before_update / t_after_update como janela de tempo do update;
                - Verificar resposta:
                    # status 200
                    # contém um modelo válido de FornecedorOnProtheusResponse
                - Verificar se o fornecedor no protheus:
                    # tem o campo version incrementado para 1
                    # tem o campo updated_at dentro da janela de tempo de atualização
                    # to_update é False

            * POST /api/v1/fornecedores-on-protheus/{id}/sync
                OBS: guardar t_before_sync / t_after_sync como janela de tempo da sincronização;
                - Verificar resposta:
                    # status 200
                    # contém um modelo válido de FornecedorOnProtheusResponse
                - Verificar se protheus_last_synced_at está dentro da janela de sincronização
                - Verificar se protheus_synced_version == version (== 1)

            No final do processo, verificar o estado consolidado do registro:
                # created_at dentro da janela de criação
                # updated_at dentro da janela de atualização (não da criação)
                # protheus_last_synced_at dentro da janela de sincronização
        """
        # ── Step 1: create fornecedor ───────────────────────────────────────
        t_before_create = datetime.now(UTC)
        response = client.post("/api/v1/fornecedores/", json={"cnpj": "11222333000181"})
        t_after_create = datetime.now(UTC)

        assert response.status_code == 201
        FornecedorResponse.model_validate(response.json())
        fornecedor_id = response.json()["id"]

        fop = fornecedor_on_protheus_repo.get_fornecedor_on_protheus_by_fornecedor_id(
            fornecedor_id, db_session
        )
        assert fop is not None
        assert_fornedor_on_protheus_created_at(fop, t_before_create, t_after_create)
        assert_fornecedor_on_protheus_updated_at(fop, t_before_create, t_after_create)
        assert fop.version == 0
        assert fop.protheus_synced_version == 0
        assert fop.to_update is False
        assert fop.protheus_last_synced_at is None

        fop_id = fop.id

        # ── Step 2: PATCH without mark-for-update → expect 403 ─────────────
        response = client.patch(
            f"/api/v1/fornecedores-on-protheus/{fop_id}",
            json={"cep": "57020-565"},
        )

        assert response.status_code == 403

        fop = fornecedor_on_protheus_repo.get_fornecedor_on_protheus_by_id(fop_id, db_session)
        assert_fornecedor_on_protheus_version(fop, 0)
        assert_fornecedor_on_protheus_updated_at(fop, t_before_create, t_after_create)
        assert fop.to_update is False

        # ── Step 3: mark for update ─────────────────────────────────────────
        response = client.post(f"/api/v1/fornecedores-on-protheus/{fop_id}/mark-for-update")

        assert response.status_code == 200
        FornecedorOnProtheusResponse.model_validate(response.json())

        fop = fornecedor_on_protheus_repo.get_fornecedor_on_protheus_by_id(fop_id, db_session)
        assert fop.to_update is True
        assert_fornecedor_on_protheus_updated_at(fop, t_before_create, t_after_create)

        # ── Step 4: PATCH update (now allowed) ──────────────────────────────
        t_before_update = datetime.now(UTC)
        response = client.patch(
            f"/api/v1/fornecedores-on-protheus/{fop_id}",
            json={"cep": "57020-565"},
        )
        t_after_update = datetime.now(UTC)

        assert response.status_code == 200
        FornecedorOnProtheusResponse.model_validate(response.json())

        fop = fornecedor_on_protheus_repo.get_fornecedor_on_protheus_by_id(fop_id, db_session)
        assert_fornecedor_on_protheus_version(fop, 1)
        assert_fornecedor_on_protheus_updated_at(fop, t_before_update, t_after_update)
        assert fop.to_update is False

        # ── Step 5: sync ────────────────────────────────────────────────────
        t_before_sync = datetime.now(UTC)
        response = client.post(f"/api/v1/fornecedores-on-protheus/{fop_id}/sync")
        t_after_sync = datetime.now(UTC)

        assert response.status_code == 200
        FornecedorOnProtheusResponse.model_validate(response.json())

        fop = fornecedor_on_protheus_repo.get_fornecedor_on_protheus_by_id(fop_id, db_session)
        assert_fornecedor_on_protheus_last_synced_at(fop, t_before_sync, t_after_sync)
        assert_fornecedor_protheus_synced_version(fop, 1)

        # ── Final consolidated state ────────────────────────────────────────
        assert_fornedor_on_protheus_created_at(fop, t_before_create, t_after_create)
        assert_fornecedor_on_protheus_updated_at(fop, t_before_update, t_after_update)
        assert_fornecedor_on_protheus_last_synced_at(fop, t_before_sync, t_after_sync)

