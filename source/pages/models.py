from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from pages.page_choice import PageChoices
from courses import HomeUpload
# Create your models here.


class PageModel(models.Model):
    title = models.CharField(verbose_name='Название страницы', 
                             null=True, 
                             unique=True, 
                             max_length=150
                             )
    path = models.CharField(verbose_name='Путь до страницы', 
                            choices=PageChoices,
                            default=PageChoices.HOME
                            )
    text_primary = CKEditor5Field(verbose_name='Основной блок', 
                                  config_name='extends', 
                                  blank=True, 
                                  null=True
                                  )
    text_secondary = CKEditor5Field(verbose_name='Дополнительный блок', 
                                    config_name='extends', 
                                    blank=True, 
                                    null=True
                                    )
    
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Тексты для страниц"
        verbose_name_plural = "Тексты для страниц"


class CarouselMainModel(models.Model):
    page = models.ForeignKey(verbose_name='Страница', related_name='main',to=PageModel, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Изображение', upload_to=HomeUpload._upload)

    class Meta:
        verbose_name = "Главная карусель"
        verbose_name_plural = "Главная карусель"


class CarouselSponsorsModel(models.Model):
    page = models.ForeignKey(verbose_name='Страница', related_name='sponsors',to=PageModel, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name='Изображение', upload_to=HomeUpload._upload)

    class Meta:
        verbose_name = "Спонсоры"
        verbose_name_plural = "Спонсоры"


class CarouselReviewsModel(models.Model):
    page = models.ForeignKey(verbose_name='Страница', related_name='comments',to=PageModel, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='Имя')
    review = models.TextField(verbose_name='Отзыв')
    image = models.ImageField(verbose_name='Изображение', upload_to=HomeUpload._upload)

    class Meta:
        verbose_name = "Отзывы"
        verbose_name_plural = "Отзывы"


class CarouselAdvantagesModel(models.Model):
    page = models.ForeignKey(verbose_name='Страница', 
                             related_name='adv', to=PageModel, on_delete=models.CASCADE)
    text = CKEditor5Field(verbose_name='Текст', 
                                    config_name='extends', 
                                    blank=True, 
                                    null=True
                                    )

    class Meta:
        verbose_name = "Статичные блоки"
        verbose_name_plural = "Статичные блоки"
