from django.db import models


class LessonTypeChoices(models.TextChoices):
    FREE = 'free'
    PAID = 'paid'


class VisitRateChoices(models.TextChoices):
    TWO = '2', '2'
    THREE = '3', '3'
    FOUR = '4', '4'
    FIVE = '5', '5'


class LessonVisitChoices(models.TextChoices):
    IN = 'Присутствовал', 'Присутствовал'
    OUT = 'Отсутствовал', 'Отсутствовал'
