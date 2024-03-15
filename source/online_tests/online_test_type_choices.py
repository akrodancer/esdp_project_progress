from django.db import models

class OnlineTestTypeChoices(models.TextChoices):
    FREE = 'free'
    PAID = 'paid'

