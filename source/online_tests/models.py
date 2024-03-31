from django.conf import settings
from django.db import models
from courses import QuestionUpload, AnswerUpload
from courses.models import Course
from .online_test_type_choices import OnlineTestTypeChoices, LanguageTypeChoices
from django.utils import timezone



class OnlineTest(models.Model):
    test_name = models.CharField(verbose_name='Название',
                                 max_length=255
                                 )
    difficulty = models.CharField(verbose_name='Сложность',
                                  max_length=40
                                  )
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    test_type = models.CharField(verbose_name='Тип',
                                 max_length=4, 
                                 choices=OnlineTestTypeChoices, 
                                 default=OnlineTestTypeChoices.FREE
                                 )
    test_language = models.CharField(verbose_name='Язык курса',
                                     max_length=10,
                                     choices=LanguageTypeChoices,
                                     default=LanguageTypeChoices.KG)
    course = models.ManyToManyField(verbose_name='Курс',
                                    to=Course, 
                                    related_name='online_tests'
                                    )
    countdown = models.DurationField(null=True, blank=True, default=None)

    def __str__(self):
        return self.test_name

    @property
    def countdown_formatted_ru(self):
        total_minutes = self.countdown.seconds // 60
        if total_minutes <= 60:
            return f"{total_minutes} минут"
        else:
            hours = self.countdown.seconds // 3600
            minutes = (self.countdown.seconds // 60) % 60
            return f"{hours} часа {minutes} минут"

    @property
    def countdown_formatted_kg(self):
        total_minutes = self.countdown.seconds // 60
        if total_minutes <= 60:
            return f"{total_minutes} мүнөт"
        else:
            hours = self.countdown.seconds // 3600
            minutes = (self.countdown.seconds // 60) % 60
            return f"{hours} саат {minutes} мүнөт"

    def is_accessible_by(self, user):

        if self.test_type == 'free':
            return True
        if self.course.is_paid_by(user):
            return True
        return False
    
    class Meta:
        verbose_name = 'Онлайн тест'
        verbose_name_plural = 'Онлайн тесты'


class Question(models.Model):
    question_name = models.CharField(verbose_name='Название',
                                     max_length=255
                                     )
    question_text = models.TextField(verbose_name='Описание',
                                    blank=True, 
                                    null=True
                                    )
    question_image = models.ImageField(verbose_name='Изображение',
                                       upload_to=QuestionUpload._upload, 
                                       blank=True, 
                                       null=True
                                       )
    test = models.ForeignKey(verbose_name='Тест',
                             to=OnlineTest, 
                             related_name='questions', 
                             on_delete=models.CASCADE
                             )

    def __str__(self):
        return self.question_name

    class Meta:
        verbose_name='Вопросы'
        verbose_name_plural='Вопросы'

class Answer(models.Model):
    is_correct = models.BooleanField(verbose_name='Правильный')
    answer_text = models.TextField(verbose_name='Описание',
                                   blank=True, 
                                   null=True
                                   )
    answer_image = models.ImageField(verbose_name='Изображение',
                                    upload_to=AnswerUpload._upload, 
                                    blank=True, 
                                    null=True
                                    )
    question = models.ForeignKey(verbose_name='Вопрос',
                                 to=Question, 
                                 related_name='answers', 
                                 on_delete=models.CASCADE
                                 )

    def __str__(self):
        return str(self.pk)
    
    class Meta:
        verbose_name='Ответ'
        verbose_name_plural='Ответ'


class UserTest(models.Model):
    user = models.ForeignKey(verbose_name='Пользователь',
                             to=settings.AUTH_USER_MODEL, 
                             related_name='user_tests', 
                             on_delete=models.CASCADE
                             )
    test = models.ForeignKey(verbose_name='Тест',
                             to=OnlineTest, 
                             related_name='user_tests', 
                             on_delete=models.CASCADE
                             )
    attempts = models.IntegerField(default=0)
    correct_answer_count = models.IntegerField(default=0)
                                          
    incorrect_answer_cnt = models.IntegerField(default=0)
    test_start = models.DateTimeField(default=timezone.now)
    test_end = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'Test {self.test} taken by {self.user}'
    
    class Meta:
        verbose_name='Тесты ученика'
        verbose_name_plural='Тесты ученика'
        unique_together = ('user', 'test')

