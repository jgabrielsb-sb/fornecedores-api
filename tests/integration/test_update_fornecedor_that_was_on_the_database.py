"""
CASE 2:
* Um fornecedor que já está no banco de dados precisa ser atualizado:
    - Criar o fornecedor via /fornecedores/create
        * verificar se retorna 409;
        
    - Marcar o fornecedor para ser atualizado via /fornedores_on_protheus/{fornecedor_on_protheus_id}/set_to_update_to_true
        * verificar se o campo to_update foi atualizado para true
        * verificar se o campo updated_at continua o mesmo

    - Atualizar o fornecedor via /fornecedores/{fornecedor_id}/update
        * verificar se o fornecedor na tabela fornecedores foi atualizado com sucesso
        * verificar se o fornecedor na tabela fornecedor_on_protheus foi atualizado com sucesso
            - version deve ser incrementado;
            - updated_at deve ser a data e hora atual;
            - campos a atualizar devem ser os passados na request;

    - Sincronizar o fornecedor via /fornecedores_on_protheus/{fornecedor_on_protheus_id}/sync
        * verificar se o campo protheus_synced_version é o mesmo que version do fornecedor_on_protheus
        * verificar se o campo protheus_last_synced_at é a data e hora atual
        * verificar se o campo updated_at continua o mesmo
        * verificar se o campo to_update é true
        * verificar se o campo to_update foi atualizado para true
        * verificar se o campo updated_at continua o mesmo
"""