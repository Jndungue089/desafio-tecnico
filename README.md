# Lead Management API

API para gerenciamento de Leads desenvolvida com **Python**, **FastAPI** e **MongoDB**.

---

## Como rodar o projeto

### Com Docker (recomendado)

```bash
docker compose up --build
```

A API estará disponível em `http://localhost:8000`.

O MongoDB é iniciado automaticamente via Docker Compose na porta `27017`.

### Sem Docker (local)

1. Inicie o MongoDB localmente na porta `27017`.
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute a aplicação:

```bash
uvicorn app.main:app --reload
```

---

## Endpoints

### POST /leads

Cria um novo lead. O campo `birth_date` é preenchido automaticamente via integração externa.

```bash
curl -X POST http://localhost:8000/leads \
  -H "Content-Type: application/json" \
  -d '{"name": "João Silva", "email": "joao@example.com", "phone": "+5511999999999"}'
```

Resposta (`201 Created`):

```json
{
  "id": "...",
  "name": "João Silva",
  "email": "joao@example.com",
  "phone": "+5511999999999",
  "birth_date": "1998-02-05"
}
```

### GET /leads

Lista todos os leads cadastrados.

```bash
curl http://localhost:8000/leads
```

### GET /leads/{id}

Retorna um lead específico pelo seu ID.

```bash
curl http://localhost:8000/leads/{id}
```

---

## Documentação interativa

O FastAPI gera documentação automática disponível em:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Arquitetura

O projeto segue uma arquitetura em camadas com separação clara de responsabilidades:

```
app/
├── api/            # Rotas / Controllers
│   └── routes.py
├── core/           # Configurações da aplicação
│   └── config.py
├── db/             # Conexão com o banco de dados
│   └── mongodb.py
├── schemas/        # Schemas Pydantic (entrada/saída)
│   └── lead.py
├── services/       # Lógica de negócio e integrações
│   ├── lead_service.py
│   └── external_api.py
└── main.py         # Ponto de entrada da aplicação
tests/
└── test_leads.py   # Testes automatizados
```

- **api/**: Define os endpoints HTTP (controllers).
- **schemas/**: Modelos Pydantic para validação de dados de entrada e formato de resposta.
- **services/**: Contém a lógica de negócio (`lead_service.py`) e a integração com a API externa (`external_api.py`).
- **db/**: Gerencia a conexão com o MongoDB via Motor (driver assíncrono).
- **core/**: Configurações centralizadas (URL do banco, URL da API externa).

---

## Integração externa

Durante a criação de um lead (`POST /leads`), o sistema consome a API pública `https://dummyjson.com/users/1` para obter o campo `birthDate`, que é armazenado como `birth_date`.

### Comportamento em caso de falha da API externa

Em caso de falha na requisição externa (timeout, erro HTTP, indisponibilidade), o lead é criado normalmente com `birth_date = null`. O sistema **não** retorna erro ao usuário — a falha é tratada silenciosamente para garantir que o cadastro do lead não seja bloqueado por uma dependência externa.

---

## Testes

Para rodar os testes automatizados:

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

Os testes utilizam `mongomock-motor` para simular o MongoDB em memória e `unittest.mock` para mockar a integração externa.
