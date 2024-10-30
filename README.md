# API de Pagamentos (Desafio Backend)

API REST para processamento de pagamentos entre usuários (lojistas e consumidores), baseada no [desafio backend do PicPay](https://github.com/PicPay/picpay-desafio-backend).

## 🚀 Tecnologias

- Python 3.11
- Django 5.1
- Django Ninja (API REST)
- Celery (Processamento Assíncrono)
- Redis (Message Broker)
- Docker & Docker Compose

## 🎯 Funcionalidades

- Cadastro de usuários (Lojistas e Consumidores)
- Validação de CPF
- Sistema de permissões baseado em roles
- Transferências entre usuários
- Notificações assíncronas via Celery
- Validação em serviço externo
- Rollback em caso de falha

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
- Documentação OpenAPI: http://localhost:8000/api/docs
- Admin Django: http://localhost:8000/admin

### Endpoints

#### Usuários
- `POST /api/users/`: Criar novo usuário
  - Tipos: people (consumidor) ou company (lojista)
  - Validação de CPF
  - Dados únicos (username, email, cpf)

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

## 🔧 Desenvolvimento

Para executar os testes:

```bash
docker-compose exec web python manage.py test
```

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
