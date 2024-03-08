from django.db import models

class PageChoices(models.TextChoices):
    HOME = '/'
    ABOUT_US = '/about_us/'
    COURSES = '/courses/'
