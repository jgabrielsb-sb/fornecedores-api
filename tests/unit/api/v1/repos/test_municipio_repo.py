from datetime import UTC, datetime

import pytest

from fornecedores_app.api.v1.models.dto_municipio import MunicipioCreate
from fornecedores_app.api.v1.repos import municipio_repo
from fornecedores_app.db.schemas import MunicipiosSchema

pytestmark = pytest.mark.unit


@pytest.fixture
def municipio_create() -> MunicipioCreate:
    return MunicipioCreate(
        municipio_name="Belo Horizonte",
        codigo_ibge="3106200",
    )


class TestCreateMunicipio:
    def test_should_create_municipio_with_valid_data(
        self,
        db_session,
        municipio_create: MunicipioCreate,
    ):
        now = datetime.now(UTC)
        municipio_returned = municipio_repo.create(
            municipio_create,
            now=now,
            session=db_session,
        )

        assert isinstance(municipio_returned, MunicipiosSchema)
        assert municipio_returned.municipio_name == municipio_create.municipio_name
        assert municipio_returned.codigo_ibge == municipio_create.codigo_ibge
        assert municipio_returned.created_at == now
        assert municipio_returned.updated_at == now
        assert municipio_returned.id is not None


class TestGetMunicipioById:
    def test_should_return_the_municipio_given_existent_id(
        self,
        db_session,
        municipio_create: MunicipioCreate,
    ):
        now = datetime.now(UTC)
        created = municipio_repo.create(municipio_create, now=now, session=db_session)

        found = municipio_repo.get_by_id(created.id, session=db_session)

        assert found is not None
        assert found.id == created.id
        assert found.municipio_name == municipio_create.municipio_name
        assert found.codigo_ibge == municipio_create.codigo_ibge

    def test_should_return_none_given_non_existent_id(self, db_session):
        assert municipio_repo.get_by_id(424242, session=db_session) is None


class TestGetMunicipioByName:
    def test_should_return_the_municipio_given_existent_name(
        self,
        db_session,
        municipio_create: MunicipioCreate,
    ):
        now = datetime.now(UTC)
        created = municipio_repo.create(municipio_create, now=now, session=db_session)

        found = municipio_repo.get_by_name(municipio_create.municipio_name, session=db_session)

        assert found is not None
        assert found.id == created.id
        assert found.municipio_name == municipio_create.municipio_name

    def test_should_return_none_given_non_existent_name(self, db_session):
        assert municipio_repo.get_by_name("Non Existent City", session=db_session) is None


class TestGetMunicipioByCodigoIbge:
    def test_should_return_the_municipio_given_existent_codigo_ibge(
        self,
        db_session,
        municipio_create: MunicipioCreate,
    ):
        now = datetime.now(UTC)
        created = municipio_repo.create(municipio_create, now=now, session=db_session)

        found = municipio_repo.get_by_codigo_ibge(municipio_create.codigo_ibge, session=db_session)

        assert found is not None
        assert found.id == created.id
        assert found.codigo_ibge == municipio_create.codigo_ibge

    def test_should_return_none_given_non_existent_codigo_ibge(self, db_session):
        assert municipio_repo.get_by_codigo_ibge("9999999", session=db_session) is None
