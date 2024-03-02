# Generated by Django 5.0.2 on 2024-03-01 20:28

import courses.image_load
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(blank=True, null=True, upload_to=courses.image_load.AvatarUpload._upload, verbose_name='Аватар'),
        ),
    ]