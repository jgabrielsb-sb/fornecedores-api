from datetime import datetime

from fornecedores_app.db.schemas.schemas import FornecedorOnProteusSchema


def assert_fornecedor_on_protheus_updated_at(
    row: FornecedorOnProteusSchema,
    t_before: datetime,
    t_after: datetime,
) -> None:
    assert row.updated_at is not None
    assert t_before <= row.updated_at <= t_after
