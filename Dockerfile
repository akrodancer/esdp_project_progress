# Используем базовый образ Python
FROM python:3.11-slim-buster

# Устанавливаем переменную окружения для Python, чтобы вывод был более приятным
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Создаем директорию для приложения
WORKDIR /src

# Копируем файлы проекта
COPY poetry.lock pyproject.toml README.md /src/

# Установка poetry и зависимостей проекта
RUN pip install --no-cache-dir poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Копируем содержимое соседней папки внутрь контейнера
COPY ./source /src/

# Выполняем миграции Django перед запуском сервера
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
