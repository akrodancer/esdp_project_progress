#!/bin/sh

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

