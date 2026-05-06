"""
CASE 3:
* Um fornecedor que já está no banco de dados precisa ser atualizado, mas o campo to_update está false:
    - Criar o fornecedor via /fornecedores/create
        * verificar se retorna 409;
        
    - Atualizar o fornecedor via /fornecedores/{fornecedor_id}/update
        * verificar se retorna 403;
        * verificar se os campos continuam o mesmo
"""