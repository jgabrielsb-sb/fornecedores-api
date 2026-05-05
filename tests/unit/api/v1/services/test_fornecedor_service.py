import pytest

from fornecedores_app.api.v1.models import FornecedorCreate
from fornecedores_app.api.v1.services import fornecedor_service
from fornecedores_app.api.v1.services.exceptions import ConflictException, NotFoundException


class TestCreateFornecedor:
    def test_should_create_fornecedor_with_valid_data(self, db_session):
        dto = FornecedorCreate(cnpj="11111111111111")
        result = fornecedor_service.create_fornecedor(dto, db_session)

        assert result.cnpj == "11111111111111"
        assert result.id is not None
        assert result.created_at is not None
        assert result.updated_at is not None

    def test_should_raise_conflict_exception_if_cnpj_already_exists(self, db_session):
        dto = FornecedorCreate(cnpj="22222222222222")
        fornecedor_service.create_fornecedor(dto, db_session)

        with pytest.raises(ConflictException):
            fornecedor_service.create_fornecedor(dto, db_session)


class TestGetFornecedorByCNPJ:
    def test_should_get_fornecedor_by_cnpj(self, db_session):
        dto = FornecedorCreate(cnpj="44444444444444")
        created = fornecedor_service.create_fornecedor(dto, db_session)

        found = fornecedor_service.get_fornecedor_by_cnpj(created.cnpj, db_session)

        assert found.cnpj == created.cnpj
        assert found.id == created.id

    def test_should_raise_not_found_exception_if_fornecedor_not_found(self, db_session):
        with pytest.raises(NotFoundException):
            fornecedor_service.get_fornecedor_by_cnpj("99999999999999", db_session)


class TestGetFornecedorById:
    def test_should_get_fornecedor_by_id(self, db_session):
        dto = FornecedorCreate(cnpj="55555555555555")
        created = fornecedor_service.create_fornecedor(dto, db_session)

        found = fornecedor_service.get_fornecedor_by_id(created.id, db_session)

        assert found.id == created.id
        assert found.cnpj == created.cnpj

    def test_should_raise_not_found_exception_if_fornecedor_not_found(self, db_session):
        with pytest.raises(NotFoundException):
            fornecedor_service.get_fornecedor_by_id(424242, db_session)
