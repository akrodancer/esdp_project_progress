from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Course(models.Model):
    course_name = models.CharField(max_length=255)
    date_start = models.DateField()
    date_finish = models.DateField()
    teacher = models.ManyToManyField(settings.AUTH_USER_MODEL, limit_choices_to={'role': 'teacher'},
                                     related_name='courses_taught')
    students = models.ManyToManyField(settings.AUTH_USER_MODEL, limit_choices_to={'role': 'user'},
                                      related_name='enrolled_courses',
                                      blank=True)
    paid_by = models.ManyToManyField(settings.AUTH_USER_MODEL, limit_choices_to={'role': 'user'},
                                     related_name='paid_courses', blank=True)

    def __str__(self):
        return self.course_name

    def is_paid_by(self, user):
        return self.paid_by == user


class Lesson(models.Model):
    class LessonType(models.TextChoices):
        FREE = 'free', _('Free')
        PAID = 'paid', _('Paid')

    lesson_name = models.CharField(max_length=255)
    grade = models.PositiveIntegerField()
    description = models.TextField(max_length=5000)
    video = models.URLField(max_length=200, null=True)
    lesson_date = models.DateTimeField()
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.SET_NULL, null=True)
    lesson_type = models.CharField(max_length=4, choices=LessonType.choices, default=LessonType.FREE)

    def __str__(self):
        return self.lesson_name

    def is_accessible_by(self, user):
        if self.lesson_type == self.LessonType.FREE:
            return True
        if self.course.is_paid_by(user):
            return True
        return False


class Visit(models.Model):
    is_currently_viewing = models.BooleanField()
    visit_date = models.DateTimeField(auto_now_add=True)
    students = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'role', 'user'}, related_name='visits',
                                 on_delete=models.CASCADE, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, related_name='visits', on_delete=models.CASCADE)

    def __str__(self):
        return f'Visit by {self.students} on {self.visit_date}'
