from fornecedores_app.db.schemas.schemas import FornecedorOnProteusSchema


def assert_fornecedor_on_protheus_version(
    row: FornecedorOnProteusSchema,
    expected_version: int,
) -> None:
    assert row.version == expected_version
