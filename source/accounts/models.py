from django.contrib.auth.models import AbstractUser
from django.db import models
from accounts.account_types import ACCOUNT_TYPES


class User(AbstractUser):
    class Meta:
        verbose_name_plural = 'Пользователи'
        
    avatar = models.ImageField(verbose_name='Аватар', upload_to='...', null=True, blank=True)
    email = models.EmailField(verbose_name='Электронная почта', unique=True)
    phone = models.CharField(verbose_name='Номер телефона', max_length=20)
    role = models.CharField(verbose_name='Должность', 
                            max_length=30, 
                            choices=ACCOUNT_TYPES,
                            default=ACCOUNT_TYPES.USER
                            )

    def __str__(self):
        return self.username


class Comment(models.Model):
    class Meta:
        verbose_name_plural = 'Комментарии'

    content = models.TextField(verbose_name='Содержание', max_length=500)
    teacher = models.ForeignKey(to=User, verbose_name='Учитель', limit_choices_to={'role': 'teacher'}, related_name='comments_given', on_delete=models.CASCADE)
    student = models.ForeignKey(to=User, verbose_name='Ученик', limit_choices_to={'role': 'user'}, related_name='comments_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='Время публикации', auto_now_add=True)
