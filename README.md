# Aquisição de dados da Câmara de Degradação - API

Essa é a API de aquição de dados do experimento. Deve rodar em um servidor e tem objetivo de recerber os dados medidos e salva-los em um base de dados SQL.

## Arquivo de configuração

Crie um arquivo `.env` na raiz do repositório. Ele deverá conter as seguintes variáveis, que configuram a aplicação:

    # exemplo de valores
    HOST=localhost
    PORT=8000
    API_PATH=/degrad/api
    DASH_PATH=/degrad/dash
    API_KEY=secret

## Execução com docker-compose

Primeiro crie um volume permanente para a base de dados

    docker volume create postgres-data

Para construir e inicializar os container rode

    docker-compose up --build

## Usando o alembic para alterar a base de dados

Precisamos rodar os seguinte comandos quando mudarmos a base de dados.

    # Primeiro reconstrua as imagens para adicionar as últimas mudanças no código
    docker-compose build
    # Gere o script de migração
    docker-compose run api alembic revision --autogenerate -m "made some changes"
    # Execute a migração. Opicional, já que a migração é executada durante a inicialição do container
    docker-compose run api alembic upgrade head

## Compose v2

Uma nova versão do docker composer foi liberada, a v2. Nesse versão os comandos são executados sem o `-`. Troque `docker-compose` por `docker compose`.

## TODO

- Backup da base de dados. [exemplo](https://simplebackups.com/blog/docker-postgres-backup-restore-guide-with-examples/)
- Backup das configurações do Grafana. [exemplo](https://stackoverflow.com/questions/45207785/how-do-i-back-up-docker-volume-for-postgres)
- Algum tipo de autenticação na API.


## Rerências

- [FastAPI behind a proxy](https://fastapi.tiangolo.com/advanced/behind-a-proxy/)
- [Grafana behind a proxy](https://stackoverflow.com/questions/49786801/using-traefik-to-reverse-proxy-grafana-at-a-suburl-404-responses)
