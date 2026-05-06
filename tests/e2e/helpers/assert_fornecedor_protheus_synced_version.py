from fornecedores_app.db.schemas.schemas import FornecedorOnProteusSchema


def assert_fornecedor_protheus_synced_version(
    row: FornecedorOnProteusSchema,
    expected_version: int,
) -> None:
    assert row.protheus_synced_version == expected_version
