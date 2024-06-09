
FROM python:3.12-slim

RUN apt-get update \
 && DEBIAN_FRONTEND=noninteractive \
    apt-get install --no-install-recommends --assume-yes \
      netcat-openbsd

RUN pip install poetry==1.6.1

RUN poetry config virtualenvs.create false

WORKDIR /code

COPY . /code

RUN poetry install --only main --no-interaction --no-ansi --no-root

CMD ["/code/start.sh"]