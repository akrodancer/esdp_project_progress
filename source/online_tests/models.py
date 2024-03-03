from django.conf import settings
from django.db import models
from courses import QuestionUpload, AnswerUpload
from courses.models import Course
from .online_test_type_choices import OnlineTestTypeChoices



class Test(models.Model):
    test_name = models.CharField(verbose_name='Название',
                                 max_length=255
                                 )
    difficulty = models.CharField(verbose_name='Сложность',
                                  max_length=40
                                  )
    test_type = models.CharField(verbose_name='Тип',
                                 max_length=4, 
                                 choices=OnlineTestTypeChoices, 
                                 default=OnlineTestTypeChoices.FREE
                                 )
    course = models.ManyToManyField(verbose_name='Курс',
                                    to=Course, 
                                    related_name='online_tests'
                                    )

    def __str__(self):
        return self.test_name

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
                             to=Test, 
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
                             to=Test, 
                             related_name='user_tests', 
                             on_delete=models.CASCADE
                             )
    date_taken = models.DateTimeField(verbose_name='Дата тестирование',
                                      auto_now_add=True
                                      )
    correct_answers = models.IntegerField(verbose_name='Правильные ответы',
                                          default=0
                                          )
    incorrect_answers = models.IntegerField(verbose_name='Неправильные ответы',
                                            default=0
                                            )

    def count_answers(self):
        answers = self.user_answers.all()
        total = answers.count()
        correct = answers.filter(answer__is_correct=True).count()
        incorrect = total - correct
        return correct, incorrect

    def update_answer_counts(self):
        correct = self.user_answers.filter(answer__is_correct=True).count()
        incorrect = self.user_answers.count() - correct
        self.correct_answers = correct
        self.incorrect_answers = incorrect
        self.save()

    def __str__(self):
        return f'Test {self.test} taken by {self.user}'
    
    class Meta:
        verbose_name='Тесты ученика'
        verbose_name_plural='Тесты ученика'


class UserAnswer(models.Model):
    user_test = models.ForeignKey(verbose_name='Тесты учеников',
                                  to=UserTest, 
                                  related_name='user_answers', 
                                  on_delete=models.CASCADE
                                  )
    question = models.ForeignKey(verbose_name='Вопросы',
                                 to=Question, 
                                 related_name='user_answers', 
                                 on_delete=models.CASCADE
                                 )
    answer = models.ForeignKey(verbose_name='Ответы',
                               to=Answer, 
                               related_name='user_answers', 
                               on_delete=models.CASCADE
                               )

    def __str__(self):
        return f'Answer by {self.user_test.user} to {self.question}'

    class Meta:
        verbose_name='Ответы учеников'
        verbose_name_plural='Ответы учеников'