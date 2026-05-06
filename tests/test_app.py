from fornecedores_app.api.main import create_app

import pytest

pytestmark = pytest.mark.unit

def test_create_app():
    app = create_app()
    assert app.title == "Fornecedores API"
