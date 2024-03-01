from django.db import models

class ACCOUNT_TYPES(models.TextChoices):
    TEACHER = 'teacher'
    USER = 'user'


    