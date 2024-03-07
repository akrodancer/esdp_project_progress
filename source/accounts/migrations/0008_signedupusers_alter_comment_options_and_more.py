# Generated by Django 5.0.2 on 2024-03-07 14:46

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_alter_comment_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='SignedUpUsers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(verbose_name='Имя')),
                ('last_name', models.CharField(verbose_name='Фамилия')),
                ('phone', models.CharField(verbose_name='Телефон')),
                ('email', models.EmailField(max_length=254, verbose_name='Электронная почта')),
                ('course', models.CharField(verbose_name='Курс')),
            ],
            options={
                'verbose_name': 'Заявки на курсы',
                'verbose_name_plural': 'Заявки на курсы',
            },
        ),
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': 'Комментарии', 'verbose_name_plural': 'Комментарии'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': 'Пользователи', 'verbose_name_plural': 'Пользователи'},
        ),
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('object', django.contrib.auth.models.UserManager()),
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]