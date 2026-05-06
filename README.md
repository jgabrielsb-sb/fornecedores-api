# Fornecedores API

API REST para gerenciamento de fornecedores e sincronização com o sistema Protheus, construída com **FastAPI**, **SQLAlchemy** e **PostgreSQL**.

---

## Sumário

- [Visão Geral](#visão-geral)
- [Pré-requisitos](#pré-requisitos)
- [Configuração do Ambiente](#configuração-do-ambiente)
- [Executando o Projeto](#executando-o-projeto)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Testes](#testes)

---

## Visão Geral

A API expõe dois recursos principais:

| Recurso | Prefixo | Descrição |
|---|---|---|
| `Fornecedor` | `/api/v1/fornecedores` | Criação e consulta de fornecedores |
| `FornecedorOnProtheus` | `/api/v1/fornecedores-on-protheus` | Controle do ciclo de atualização e sincronização com o Protheus |

O ciclo de vida de um fornecedor no Protheus segue o fluxo:

```
POST /fornecedores/          →   cria o fornecedor (version=0, to_update=False)
POST /{id}/mark-for-update   →   habilita atualização (to_update=True)
PATCH /{id}                  →   aplica os dados novos (version+1, to_update=False)
POST /{id}/sync              →   confirma sincronização com o Protheus
```

A documentação interativa da API está disponível em `/api/docs` após iniciar o servidor.

---

## Pré-requisitos

- **Python 3.11+**
- **[uv](https://github.com/astral-sh/uv)** — gerenciador de pacotes e ambientes virtuais
- **PostgreSQL** — banco de dados principal (duas instâncias: dev e test)
- **make** — para os comandos do Makefile

---

## Configuração do Ambiente

### 1. Instalar dependências

```bash
uv sync
```

### 2. Configurar as variáveis de ambiente

Copie o arquivo de exemplo e preencha com os dados do seu ambiente:

```bash
cp .env.sample .env
```

`.env` — ambiente de desenvolvimento:

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fornecedores_api_dev

API_VERSION=0.0.1
API_PREFIX=/api
```

`.env.test` — ambiente de testes e2e (já incluso no repositório):

```env
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME=fornecedores_protheus_test
```

> **Importante:** o nome do banco de testes precisa conter a palavra `test`. A aplicação verifica isso automaticamente antes de qualquer teste e2e para evitar execução acidental no banco de produção.

### 3. Criar o banco de dados e aplicar as migrations

Com o PostgreSQL em execução, aplique as migrations via Alembic:

```bash
uv run alembic upgrade head
```

---

## Executando o Projeto

```bash
uv run python src/run_api.py
```

A API ficará disponível em `http://localhost:8000`.  
Documentação Swagger: `http://localhost:8000/api/docs`

---

## Estrutura do Projeto

```
fornecedores-api/
├── src/
│   └── fornecedores_app/
│       ├── api/
│       │   ├── fields/              # Tipos Pydantic customizados (CEPField, CNPJField)
│       │   ├── main.py              # Factory da aplicação FastAPI e handlers de exceção
│       │   └── v1/
│       │       ├── controllers/     # Routers FastAPI (entrada HTTP)
│       │       ├── models/          # DTOs Pydantic (request/response)
│       │       ├── repos/           # Acesso ao banco de dados (SQLAlchemy queries)
│       │       ├── services/        # Regras de negócio
│       │       └── v1_router.py     # Agrupamento dos routers de v1
│       ├── config/                  # Configurações via pydantic-settings (.env)
│       └── db/
│           ├── schemas/             # Modelos ORM (SQLAlchemy declarative)
│           ├── scripts/             # Scripts utilitários de banco
│           └── session.py           # Engine e fábrica de sessões
├── tests/
│   ├── conftest.py                  # Configuração global (APP_ENV, DB_NAME)
│   ├── unit/                        # Testes unitários (SQLite em memória)
│   │   └── api/v1/
│   │       ├── conftest.py          # Engine SQLite e fixture db_session
│   │       ├── repos/               # Testes dos repositórios
│   │       └── services/            # Testes dos serviços
│   ├── e2e/                         # Testes end-to-end (PostgreSQL de teste)
│   │   ├── conftest.py              # Engine PostgreSQL, fixtures db_session e client
│   │   ├── cases/                   # Cenários de teste completos
│   │   └── helpers/                 # Funções de asserção reutilizáveis
│   └── integration/                 # Testes de integração
├── alembic/                         # Migrations de banco de dados
├── pyproject.toml                   # Dependências e configuração do pytest
└── Makefile                         # Comandos de desenvolvimento
```

### Camadas da aplicação

A arquitetura segue um fluxo em camadas bem definido:

```
Controller  →  Service  →  Repo  →  DB
```

| Camada | Responsabilidade |
|---|---|
| **Controller** | Recebe a requisição HTTP, valida o payload e delega para o service |
| **Service** | Aplica as regras de negócio, orquestra chamadas ao repo e commita a transação |
| **Repo** | Executa as queries SQLAlchemy; não conhece regras de negócio |
| **DB (schemas)** | Define os modelos ORM mapeados para as tabelas do PostgreSQL |

---

## Testes

### Organização

Os testes estão divididos em três categorias, cada uma com seu próprio marcador pytest:

| Categoria | Marcador | Banco de dados | Localização |
|---|---|---|---|
| **Unitários** | `unit` | SQLite em memória | `tests/unit/` |
| **E2E** | `e2e` | PostgreSQL (`*_test`) | `tests/e2e/` |
| **Integração** | `integration` | — | `tests/integration/` |

#### Testes unitários (`unit`)

Cobrem repositórios e serviços de forma isolada. Usam um banco SQLite em memória criado e descartado a cada sessão de testes. Cada teste recebe uma sessão enrolada em uma `SAVEPOINT` que é revertida ao final, garantindo isolamento total sem necessidade de truncar tabelas.

Estão organizados espelhando a estrutura do `src/`:

```
tests/unit/api/v1/
├── repos/     # testa as queries do repo diretamente
└── services/  # testa as regras de negócio com o banco real (SQLite)
```

#### Testes e2e (`e2e`)

Exercitam fluxos completos através da API HTTP, usando o `TestClient` do FastAPI contra o banco PostgreSQL de teste. O mesmo mecanismo de `SAVEPOINT` garante que nenhum dado persiste entre os testes.

```
tests/e2e/
├── conftest.py        # engine PostgreSQL, fixtures db_session e client
├── cases/             # cenários de teste (um arquivo por fluxo de negócio)
└── helpers/           # funções de asserção reutilizáveis entre os cenários
```

Os helpers encapsulam asserções específicas de campos do `FornecedorOnProtheus` (ex.: `assert_fornecedor_on_protheus_updated_at`, `assert_fornecedor_on_protheus_version`), permitindo que os cenários de teste fiquem legíveis e focados no fluxo.

### Comandos Make

| Comando | Descrição |
|---|---|
| `make test-unit` | Executa apenas os testes unitários |
| `make test-e2e` | Executa apenas os testes e2e (requer PostgreSQL de teste em execução) |
| `make clean` | Remove arquivos `__pycache__` e `.pyc` do projeto |

```bash
# Rodar testes unitários
make test-unit

# Rodar testes e2e
make test-e2e

# Rodar todos os testes
make test-all
```



> Os testes e2e requerem que o banco definido em `.env.test` esteja disponível e que seu nome contenha a palavra `test`. O comando `make test-e2e` já injeta `APP_ENV=test` automaticamente.

### Executar todos os testes de uma vez

```bash
APP_ENV=test uv run pytest
```

### Executar por marcador manualmente

```bash
# Apenas unitários
uv run pytest -m unit

# Apenas e2e
APP_ENV=test uv run pytest -m e2e
```
