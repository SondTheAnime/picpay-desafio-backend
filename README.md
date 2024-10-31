# API de Pagamentos (Desafio Backend)

API REST para processamento de pagamentos entre usuários (lojistas e consumidores), baseada no [desafio backend do PicPay](https://github.com/PicPay/picpay-desafio-backend).

## 🚀 Tecnologias

- Python 3.11
- Django 5.1
- Django Ninja (API REST)
- Celery (Processamento Assíncrono)
- Redis (Message Broker e Cache)
- Docker & Docker Compose

## 🎯 Funcionalidades

- Cadastro de usuários (Lojistas e Consumidores)
- Validação de CPF
- Sistema de permissões baseado em roles
- Transferências entre usuários
- Notificações assíncronas via Celery
- Sistema de filas com Celery
- Validação em serviço externo
- Rollback em caso de falha
- Cache de dados com Redis


## 🛠️ Configuração

1. Clone o repositório:

```bash
git clone https://github.com/SondTheAnime/picpay-desafio-backend.git
cd picpay-desafio-backend
```

2. Configure as variáveis de ambiente:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate  # Windows
```

3. Construa e inicie os containers:

```bash
docker compose up --build
```

## 📚 Documentação da API

Após iniciar o projeto, acesse:
- Documentação OpenAPI: http://localhost:8001/api/docs
- Admin Django: http://localhost:8001/admin

### Endpoints

#### Usuários
- `POST /api/users/`: Criar novo usuário
  - Tipos: people (consumidor) ou company (lojista)
  - Validação de CPF
  - Dados únicos (username, email, cpf)
- `GET /api/users/{id}`: Buscar usuário
  - Cache implementado (TTL: 5 minutos)
  - Retorna dados básicos do usuário

#### Pagamentos
- `POST /api/payments/`: Realizar transferência
  - Validação de saldo
  - Verificação de permissões
  - Autorização externa
  - Notificação assíncrona

## 🧪 Regras de Negócio

1. Usuários
   - Consumidor: pode enviar e receber transferências
   - Lojista: apenas recebe transferências

2. Transferências
   - Validação de saldo do pagador
   - Autorização via serviço externo
   - Rollback em caso de falha
   - Notificação aos envolvidos

3. Cache
   - Implementado para consultas de usuários
   - TTL: 5 minutos
   - Invalidação automática em atualizações

## 🔧 Desenvolvimento

Para executar os testes:

```bash
docker-compose exec web python manage.py test
```

Para monitorar o Redis:

```bash
docker-compose exec redis redis-cli
> MONITOR  # Para ver operações em tempo real
> KEYS *   # Para listar todas as chaves
```

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
