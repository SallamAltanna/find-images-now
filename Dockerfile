FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml /app/

COPY src /app/src
COPY api /app/api
COPY utils /app/utils

RUN pip install --no-cache-dir .

EXPOSE 8945

ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "uvicorn api.main:app --host ${APP_HOST:-0.0.0.0} --port ${APP_PORT:-8945}"]
