from django.db import models

class AccoutTypeChoices(models.TextChoices):
    TEACHER = 'teacher'
    USER = 'user'


    