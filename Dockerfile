FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libc-dev \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

COPY . /app/

ENV PYTHONPATH="${PYTHONPATH}:/app/aggregation"

WORKDIR /app

CMD ["python", "bot/main.py"]
