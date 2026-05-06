from datetime import datetime

from fornecedores_app.db.schemas.schemas import FornecedorOnProteusSchema


def assert_fornecedor_on_protheus_last_synced_at(
    row: FornecedorOnProteusSchema,
    t_before: datetime,
    t_after: datetime,
) -> None:
    assert row.protheus_last_synced_at is not None
    assert t_before <= row.protheus_last_synced_at <= t_after
