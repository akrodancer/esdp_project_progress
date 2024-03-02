from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
# Create your models here.


class PageFlatText(models.Model):
    title = models.CharField('Название страницы', null=True, unique=True, max_length=150)
    path = models.CharField('Путь до страницы', null=True, unique=True, max_length=150)
    text_primary = CKEditor5Field('Основной блок', config_name='extends', blank=True, null=True)
    text_secondary = CKEditor5Field('Дополнительный блок', config_name='extends', blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тексты для страниц"
        verbose_name_plural = "Тексты для страниц"


