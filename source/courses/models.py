from django.db import models

from accounts.models import User


class Course(models.Model):
    course_name = models.CharField(max_length=255)
    date_start = models.DateField()
    date_finish = models.DateField()
    teacher = models.ManyToManyField(User, limit_choices_to={'role': 'teacher'}, related_name='courses_taught')
    students = models.ManyToManyField(User, limit_choices_to={'role': 'user'}, related_name='enrolled_courses',
                                      blank=True)
    paid_by = models.ManyToManyField(User, limit_choices_to={'role': 'user'}, related_name='paid_courses', blank=True)

    def __str__(self):
        return self.course_name

    def is_paid_by(self, user):
        return self.paid_by.filter(pk=user.pk).exists()


class Lesson(models.Model):
    LESSON_TYPES = (
        ('free', 'Free'),
        ('paid', 'Paid'),
    )
    lesson_name = models.CharField(max_length=255)
    grade = models.PositiveIntegerField()
    description = models.TextField(max_length=5000)
    video = models.URLField(max_length=200, null=True)
    datetime = models.DateTimeField()
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.SET_NULL, null=True)
    lesson_type = models.CharField(max_length=4, choices=LESSON_TYPES, default='free')

    def __str__(self):
        return self.lesson_name

    def is_accessible_by(self, user):

        if self.lesson_type == 'free':
            return True
        if self.course.is_paid_by(user):
            return True
        return False


class Visit(models.Model):
    is_currently_viewing = models.BooleanField()
    visit_date = models.DateTimeField(auto_now_add=True)
    students = models.ForeignKey(User, limit_choices_to={'role', 'user'}, related_name='visits',
                                 on_delete=models.SET_NULL, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, related_name='visits', on_delete=models.CASCADE)

    def __str__(self):
        return f'Visit by {self.students} on {self.visit_date}'
