from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Meta:
        verbose_name_plural = 'Пользователи'
        
    avatar = models.ImageField(upload_to='...', null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username


class Comment(models.Model):
    content = models.TextField(max_length=500)
    teacher = models.ForeignKey(User, limit_choices_to={'role': 'teacher'}, related_name='comments_given', on_delete=models.CASCADE)
    student = models.ForeignKey(User, limit_choices_to={'role': 'user'}, related_name='comments_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
