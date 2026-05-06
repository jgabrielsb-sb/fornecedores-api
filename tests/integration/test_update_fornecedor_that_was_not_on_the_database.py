"""
CASE 1:
* Um fornecedor que ainda não está no banco de dados precisa ser atualizado:
    - Criar o fornecedor via /fornecedores/create
        * verificar se o fornecedor na tabela fornecedores foi criado com sucesso
        * verificar se o fornecedor na tabela fornecedor_on_protheus foi criado com sucesso
            - version deve ser 0;
            - to_update deve ser false;
            - protheus_synced_version deve ser 0;
            - protheus_last_synced_at deve ser None;
    - Atualizar o campo to_update para true via /fornedores_on_protheus/{fornecedor_on_protheus_id}/set_to_update_to_true
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
"""