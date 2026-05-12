import pytest

from fornecedores_app.api.v1.models.dto_municipio import MunicipioCreate
from fornecedores_app.api.v1.services import municipio_service
from fornecedores_app.api.v1.services.exceptions import ConflictException, NotFoundException

pytestmark = pytest.mark.unit


class TestCreateMunicipio:
    def test_should_create_municipio_with_valid_data(self, db_session):
        dto = MunicipioCreate(municipio_name="Belo Horizonte", codigo_ibge="3106200")
        result = municipio_service.create_municipio(dto, db_session)

        assert result.municipio_name == "BELO HORIZONTE"
        assert result.codigo_ibge == "3106200"
        assert result.id is not None
        assert result.created_at is not None
        assert result.updated_at is not None

    def test_should_raise_conflict_exception_if_codigo_ibge_already_exists(self, db_session):
        dto = MunicipioCreate(municipio_name="Belo Horizonte", codigo_ibge="3106201")
        municipio_service.create_municipio(dto, db_session)

        with pytest.raises(ConflictException):
            municipio_service.create_municipio(dto, db_session)


class TestGetMunicipioById:
    def test_should_get_municipio_by_id(self, db_session):
        dto = MunicipioCreate(municipio_name="Sao Paulo", codigo_ibge="3550308")
        created = municipio_service.create_municipio(dto, db_session)

        found = municipio_service.get_municipio_by_id(created.id, db_session)

        assert found.id == created.id
        assert found.municipio_name == created.municipio_name
        assert found.codigo_ibge == created.codigo_ibge

    def test_should_raise_not_found_exception_if_municipio_not_found(self, db_session):
        with pytest.raises(NotFoundException):
            municipio_service.get_municipio_by_id(424242, db_session)


class TestGetMunicipioByName:
    def test_should_get_municipio_by_name(self, db_session):
        dto = MunicipioCreate(municipio_name="Rio de Janeiro", codigo_ibge="3304557")
        created = municipio_service.create_municipio(dto, db_session)

        found = municipio_service.get_municipio_by_name("Rio de Janeiro", db_session)

        assert found.id == created.id
        assert found.municipio_name == "RIO DE JANEIRO"

    def test_should_raise_not_found_exception_if_municipio_not_found(self, db_session):
        with pytest.raises(NotFoundException):
            municipio_service.get_municipio_by_name("Non Existent City", db_session)


class TestGetMunicipioByCodigoIbge:
    def test_should_get_municipio_by_codigo_ibge(self, db_session):
        dto = MunicipioCreate(municipio_name="Salvador", codigo_ibge="2927408")
        created = municipio_service.create_municipio(dto, db_session)

        found = municipio_service.get_municipio_by_codigo_ibge("2927408", db_session)

        assert found.id == created.id
        assert found.codigo_ibge == "2927408"

    def test_should_raise_not_found_exception_if_municipio_not_found(self, db_session):
        with pytest.raises(NotFoundException):
            municipio_service.get_municipio_by_codigo_ibge("9999999", db_session)
