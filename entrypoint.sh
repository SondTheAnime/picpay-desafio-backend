#!/bin/bash

# Tenta matar o processo na porta 8000 usando fuser ao invés de lsof
fuser -k 8000/tcp 2>/dev/null || true

# Espera o Redis estar pronto
until python -c "import redis; redis.Redis(host='redis', port=6379).ping()"
do
  echo "Aguardando Redis..."
  sleep 1
done

# Executa o comando passado pelo docker-compose
exec "$@"