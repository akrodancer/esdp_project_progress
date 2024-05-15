FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /src

COPY poetry.lock pyproject.toml README.md /src/

RUN python3 -m pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY ./source /src

EXPOSE 8000

RUN chmod +x init_and_run.sh

ENTRYPOINT ["sh", "init_and_run.sh"]
