from fornecedores_app.api.main import create_app


def test_create_app():
    app = create_app()
    assert app.title == "Fornecedores API"
