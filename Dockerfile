FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /src

COPY poetry.lock pyproject.toml README.md /src/

# Устанавливаем Poetry
RUN python3 -m pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY ./source /src/

CMD ["sh", "-c", "python manage.py migrate"]