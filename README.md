# Aquisição de dados da Câmara de Degradação - API

Essa é a API de aquição de dados do experimento. Deve rodar em um servidor e tem objetivo de recerber os dados medidos e salva-los em um base de dados SQL.

## Instalação usando `virtualenv`

Primeiro instale o `virtualenv` e crie um novo ambiente

    pip install --user virtualenv
    virtualenv venv

Ative o novo ambiente e instale as dependências

    source venv/bin/activate
    pip install -r requirements.txt

## Executando

    uvicorn app.main:app --reload

ou execute o script `run.sh`
