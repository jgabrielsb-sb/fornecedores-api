from sqlalchemy import text
from sqlalchemy.orm import Session

from fornecedores_app.api.v1.models.dto_fornecedor_to_update import FornecedorToUpdateResponse


def get(session: Session) -> list[FornecedorToUpdateResponse]:
    query = text("""
    SELECT A.A2_COD AS CODIGO, A.A2_LOJA AS LOJA, A.A2_NOME AS NOME, A.A2_NREDUZ AS NOME_FANTASIA, A.A2_CGC AS CPF_CNPJ
    FROM SA2010 A
    WHERE (A.D_E_L_E_T_ = '')
    AND (A.A2_TIPO = 'J')
    AND ((A.A2_FILIAL + A.A2_COD + A.A2_LOJA) NOT IN (
        SELECT XP_UNICO FROM SXP010
        WHERE (D_E_L_E_T_ = '') AND (XP_ALIAS = 'SA2') AND (XP_DATA >= CONVERT(VARCHAR(8),GETDATE()-30,112))
        GROUP BY XP_UNICO)
    )
    AND (A.A2_DIRETOR NOT IN ('C','F','G','D'))
    AND (A.A2_MSBLQL <> '1')
    ORDER BY A.A2_COD, A.A2_LOJA
    """)
    rows = session.execute(query).fetchall()
    return [FornecedorToUpdateResponse.model_validate(dict(row._mapping)) for row in rows]
