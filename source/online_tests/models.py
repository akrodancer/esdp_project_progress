from django.conf import settings
from django.db import models

from courses import QuestionUpload, AnswerUpload
from courses.models import Course
from .online_test_types import ONLINE_TEST_TYPES


class OnlineTest(models.Model):
    class Meta:
        verbose_name = 'Онлайн тест'
        verbose_name_plural = 'Онлайн тесты'

    test_name = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=40)
    test_type = models.CharField(max_length=4, choices=ONLINE_TEST_TYPES,
                                 default=ONLINE_TEST_TYPES.FREE)
    course = models.ManyToManyField(Course, related_name='online_tests')

    countdown = models.DurationField(null=True, blank=True, default=None)

    def __str__(self):
        return self.test_name

    def is_accessible_by(self, user):

        if self.test_type == 'free':
            return True
        if self.course.is_paid_by(user):
            return True
        return False


class Question(models.Model):
    question_name = models.CharField(max_length=255)
    question_text = models.TextField(max_length=2500, blank=True, null=True)
    question_image = models.ImageField(upload_to=QuestionUpload._upload, blank=True, null=True)
    test = models.ForeignKey(to=OnlineTest, related_name='questions', on_delete=models.CASCADE)

    def __str__(self):
        return self.question_name


class Answer(models.Model):
    is_correct = models.BooleanField()
    answer_text = models.TextField(max_length=2500, blank=True, null=True)
    answer_image = models.ImageField(upload_to=AnswerUpload._upload, blank=True, null=True)
    question = models.ForeignKey(to=Question, related_name='answers', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)


class UserTest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    correct_answer_count = models.IntegerField(default=0)
    incorrect_answer_cnt = models.IntegerField(default=0)
    test = models.ForeignKey(to=OnlineTest, related_name='user_tests', on_delete=models.CASCADE, blank=True,
                             null=True)
    attempts = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user', 'test')
