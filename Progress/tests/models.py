from django.db import models
from accounts.models import User, Test

class Test(models.Model):
    TEST_TYPES = (
        ('free', 'Free'),
        ('paid', 'Paid'),
    )
    test_name = models.CharField(max_length=255)
    difficulty = models.CharField(max_length=40)
    test_type = models.CharField(max_length=4, choices=TEST_TYPES, default='free')

    def __str__(self):
        return self.test_name

class Question(models.Model):
    question_name = models.CharField(max_length=255)
    test = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)

    def __str__(self):
        return self.question_name


class Answer(models.Model):
    is_correct = models.BooleanField()
    answer_text = models.TextField(max_length=2500)
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)

    def __str__(self):
        return self.pk


class UserTest(models.Model):
    user = models.ForeignKey(User, related_name='user_tests', on_delete=models.CASCADE)
    test = models.ForeignKey(Test, related_name='user_tests', on_delete=models.CASCADE)
    date_taken = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Test {self.test} taken by {self.user}'


class UserAnswer(models.Model):
    user_test = models.ForeignKey(UserTest, related_name='user_answers', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='user_answers', on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, related_name='user_answers', on_delete=models.CASCADE)

    def __str__(self):
        return f'Answer by {self.user_test.user} to {self.question}'
