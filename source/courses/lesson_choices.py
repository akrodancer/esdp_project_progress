from django.db import models

class LessonTypeChoices(models.TextChoices):
    FREE = 'free'
    PAID = 'paid'



