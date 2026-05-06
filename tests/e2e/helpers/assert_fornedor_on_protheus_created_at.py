from datetime import datetime

from fornecedores_app.db.schemas.schemas import FornecedorOnProteusSchema


def assert_fornedor_on_protheus_created_at(
    row: FornecedorOnProteusSchema,
    t_before: datetime,
    t_after: datetime,
) -> None:
    assert row.created_at is not None
    assert t_before <= row.created_at <= t_after
