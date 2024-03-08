from django.contrib.auth.models import AbstractUser
from django.db import models
from .account_type_choices import AccoutTypeChoices
from .user_queryset import CustomUserManager
from courses import AvatarUpload
from django.contrib.auth.models import UserManager
    

class User(AbstractUser):
    avatar = models.ImageField(verbose_name='Аватар', upload_to=AvatarUpload._upload, null=True, blank=True)
    email = models.EmailField(verbose_name='Электронная почта', unique=True)
    phone = models.CharField(verbose_name='Номер телефона', max_length=20)
    role = models.CharField(verbose_name='Должность', 
                            max_length=30, 
                            choices=AccoutTypeChoices,
                            default=AccoutTypeChoices.USER
                            )
    
    object = UserManager()
    user_set = CustomUserManager()
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name='Пользователи'
        verbose_name_plural = 'Пользователи'


class Comment(models.Model):
    content = models.TextField(verbose_name='Содержание')
    teacher = models.ForeignKey(to=User, verbose_name='Учитель', limit_choices_to={'role': 'teacher'}, related_name='comments_given', on_delete=models.CASCADE)
    student = models.ForeignKey(to=User, verbose_name='Ученик', limit_choices_to={'role': 'user'}, related_name='comments_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(verbose_name='Время публикации', auto_now_add=True)
    
    class Meta:
        verbose_name='Комментарии'
        verbose_name_plural='Комментарии'


class SignedUpUsers(models.Model):
    first_name = models.CharField(verbose_name='Имя')
    last_name = models.CharField(verbose_name='Фамилия')
    phone = models.CharField(verbose_name='Телефон')
    email = models.EmailField(verbose_name='Электронная почта')
    course = models.CharField(verbose_name='Курс')
    
    def __str__(self) -> str:
        return f'{self.first_name}, {self.last_name}'
    
    class Meta:
        verbose_name='Заявки на курсы'
        verbose_name_plural='Заявки на курсы'