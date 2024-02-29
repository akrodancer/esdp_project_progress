from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Meta:
        verbose_name_plural = 'Пользователи'
        
    avatar = models.ImageField('Аватар', upload_to='...', null=True, blank=True)
    email = models.EmailField('Электронная почта', unique=True)
    phone = models.CharField('Номер телефона', max_length=20)
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('user', 'User'),
    )
    role = models.CharField('Должность', max_length=30, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username


class Comment(models.Model):
    class Meta:
        verbose_name_plural = 'Комментарии'

    content = models.TextField('Содержание', max_length=500)
    teacher = models.ForeignKey(User, verbose_name='Учитель', limit_choices_to={'role': 'teacher'}, related_name='comments_given', on_delete=models.CASCADE)
    student = models.ForeignKey(User, verbose_name='Ученик', limit_choices_to={'role': 'user'}, related_name='comments_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField('Время публикации', auto_now_add=True)
