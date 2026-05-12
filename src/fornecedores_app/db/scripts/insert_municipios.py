import os
from datetime import UTC, datetime

import xlrd

from fornecedores_app.api.v1.models.dto_municipio import MunicipioCreate
from fornecedores_app.api.v1.repos import municipio_repo
from fornecedores_app.db.session import session_maker

_DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "municipios.xls")

_HEADER_ROW = 6
_DATA_START_ROW = 7
_COL_CODIGO_IBGE = 7
_COL_NOME_MUNICIPIO = 8


def _read_codigo_ibge(sheet: xlrd.sheet.Sheet, row: int) -> str:
    cell = sheet.cell(row, _COL_CODIGO_IBGE)
    if cell.ctype == xlrd.XL_CELL_NUMBER:
        return str(int(cell.value))
    return str(cell.value).strip()


def insert_municipios() -> None:
    wb = xlrd.open_workbook(_DATA_FILE)
    ws = wb.sheet_by_index(0)

    inserted = 0
    skipped = 0

    with session_maker() as session:
        for row_idx in range(_DATA_START_ROW, ws.nrows):
            nome = str(ws.cell_value(row_idx, _COL_NOME_MUNICIPIO)).strip()
            codigo_ibge = _read_codigo_ibge(ws, row_idx)

            if not nome or not codigo_ibge:
                continue

            if municipio_repo.get_by_codigo_ibge(codigo_ibge, session):
                skipped += 1
                continue

            municipio_repo.create(
                MunicipioCreate(municipio_name=nome, codigo_ibge=codigo_ibge),
                now=datetime.now(UTC),
                session=session,
            )
            inserted += 1

        session.commit()

    print(f"Municipios inserted: {inserted}, skipped (already exist): {skipped}")


if __name__ == "__main__":
    insert_municipios()
