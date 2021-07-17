FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim

RUN apt-get update && apt-get install -y netcat

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY ./app /app/app
COPY ./prestart.sh /app
