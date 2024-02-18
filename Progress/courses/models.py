from django.db import models
from accounts.models import User

class Course(models.Model):
    course_name = models.CharField(max_length=255)
    date_start = models.DateField()
    date_finish = models.DateField()
    teacher = models.ForeignKey(User, related_name='courses_taught', on_delete=models.CASCADE)
    students = models.ManyToManyField(User, related_name='enrolled_courses')

    def __str__(self):
        return self.name


class Lesson(models.Model):
    lesson_name = models.CharField(max_length=255)
    grade = models.PositiveIntegerField()
    description = models.TextField(max_length=5000)
    video = models.URLField(max_length=200, null=True)
    datetime = models.DateTimeField()

    def __str__(self):
        return self.lesson_name


class Visit(models.Model):
    is_active = models.BooleanField()
    visit_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='visits', on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='visits', on_delete=models.CASCADE)

    def __str__(self):
        return f'Visit by {self.user} on {self.visit_date}'
