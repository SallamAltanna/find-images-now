FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8945

ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "uvicorn api.main:app --host ${APP_HOST:-0.0.0.0} --port ${APP_PORT:-8945}"]