# Aquisição de dados da Câmara de Degradação - API

Essa é a API de aquição de dados do experimento. Deve rodar em um servidor e tem objetivo de recerber os dados medidos e salva-los em um base de dados SQL.

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
