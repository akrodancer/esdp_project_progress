from django.contrib.auth.models import AbstractUser
from django.db import models
from tests.models import Test


class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    ROLE_CHOICES = (
        ('teacher', 'Teacher'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=30, choices=ROLE_CHOICES)
    paid_tests = models.ManyToManyField(Test, blank=True)

    def __str__(self):
        return self.username
