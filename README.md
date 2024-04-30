# Прогресс

Прогресс - это образовательный центр, который предоставляет информацию о преподавательском составе, курсах и онлайн тестах по различным предметам. Сайт предназначен для школьников, студентов и родителей, которые могут получить всю необходимую информацию о курсах, преподавателях, а также оставить заявку на обучение. 

##  Содержание
1. [Технологии]
2. [Конфигурация]
3. [Запуск]
4. [Использование]
5. [Авторы]

## [Технологии]
- django 5.0.2
- django-Jet-Reboot 1.3.7
- django-ckeditork-5 0.2.11
- psycopg2-binary 2.9.9
- django-filter 23.5
- djangorestframework 3.14.0
- postgreSQL 14.3

## [Конфигурация]

В репозитории находиться файл example.env в котором можно сконфигурировать настройки базы данных, а также переключение Debug режима и ALLOWED_HOSTS:

```bash
SECRET_KEY=

DB_NAME=postgres
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db_1
DB_PORT=5432

ALLOWED_HOSTS=
CSRF_TRUSTED_ORIGINS=
DEBUG=True
```

## [Запуск]

Для запуска приложения необходимо наличие установленноо Docker и Docker-compose на вашей системе. Проект используем docker-compose.yaml для конфигурации сборки и запуска контейнеров приложения: 

```bash
version: '3.8'

services:
  db_1:
    container_name: db_1
    ports:
      - "5432:5432"
    image: postgres:14.3-alpine
    restart: always
    volumes:
      - ./db:/var/lib/postgresql/data 
      - ./db_backup:/docker-entrypoint-initdb.d
    env_file:
      - .env
    environment:
        - POSTGRES_DB=${DB_NAME}
        - POSTGRES_PASSWORD=${DB_PASSWORD}
        - POSTGRES_USER=${DB_USER}
  web:
    container_name: progress
    build: ./
    volumes:
      - ./source:/src
    ports:
      - "8000:8000"
    restart: always
    depends_on:
      - db_1
    environment:
      - DATABASE_URL=postgres://${DB_USER}:${DB_PASSWORD}@db_1:5432/postgres
    env_file: .env

volumes:
  db_backup:
```
PostreSQL устанавливается из готового образа на Docker Hub, само приложение собирается их исходного кода с помощью Dockerfile'a в корне проекта:

```bash
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /src

COPY poetry.lock pyproject.toml README.md /src/

# Устанавливаем Poetry
RUN python3 -m pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

COPY ./source /src

ENTRYPOINT ["sh", "init_and_run.sh"]
```
Dockerfile в конце сборки запускает init_and_start.sh, который применяет существующие миграции в базу данных, создает учетную запись администратора и запускает локальный сервер:

```bash
# Создаем миграции и применяем их
python manage.py makemigrations
python manage.py migrate

# Создаем суперпользователя, если его не существует
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
EOF

# Запускаем Django сервер
python manage.py runserver 0.0.0.0:8000
```

### Команда для запуска проекта

```bash
sudo docker-compose up
```


## [Использование]

После установки и запуска сервера вы можете получить доступ к следующим функциям:

- Просмотр списка курсов и преподавателей.
- Регистрация на курсы.
- Прохождение онлайн тестов по различным предметам.
- Просмотр видеозаписей уроков.

Для более удобного администрирования сайтов мы используем Django Jet Admin.


## [Авторы]

- Сагидуллин Эмиль - emil.sagidullin@mail.ru
- Юрмашев Радмир - barrberry666@gmail.com
- Барханский Кирилл - kulgansad@gmail.com
- Охлопков Гаврил - gokhlopkov2002@gmail.com
- Вершинский Дмитрий- dmitrii.vershinskii@gmail.com

