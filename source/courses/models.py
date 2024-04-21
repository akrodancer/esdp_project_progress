from django.core.validators import MaxValueValidator
from django.db import models
from .lesson_choices import LessonTypeChoices, VisitRateChoices, LessonVisitChoices
from . import CourseUpload
from accounts.models import User
from django.contrib.auth import get_user_model


class Course(models.Model):
    course_name = models.CharField(verbose_name='Название курса',
                                   max_length=255
                                   )
    description = models.TextField(verbose_name='Описание',
                                   max_length=5000,
                                   null=True,
                                   blank=True
                                   )
    date_start = models.DateField(verbose_name='Дата начала')
    date_finish = models.DateField(verbose_name='Дата окончания')
    course_image = models.ImageField('Изображение',
                                     upload_to=CourseUpload._upload,
                                     null=True,
                                     blank=True
                                     )
    teacher = models.ManyToManyField(to=User, verbose_name='Учители',
                                     limit_choices_to={'role': 'teacher'},
                                     related_name='courses_taught'
                                     )
    students = models.ManyToManyField(to=User, verbose_name='Ученики',
                                      limit_choices_to={'role': 'user'},
                                      related_name='enrolled_courses',
                                      blank=True
                                      )
    paid_by = models.ManyToManyField(to=User, verbose_name='Те, кто оплатил',
                                     limit_choices_to={'role': 'user'},
                                     related_name='paid_courses',
                                     blank=True
                                     )

    class Meta:
        verbose_name = "Курсы"
        verbose_name_plural = "Курсы"

    def __str__(self):
        return self.course_name

    def is_paid_by(self, user):
        return self.paid_by.filter(pk=user.pk).exists()


class Group(models.Model):
    name = models.CharField(verbose_name='Название группы',
                                   max_length=255,
                                   null=True,
                                   blank=True)
    course = models.ForeignKey(to=Course,
                               verbose_name='Курс',
                               related_name='course_for_group',
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True
                               )
    teacher = models.ForeignKey(to=User,
                                verbose_name='Учитель',
                                related_name='teacher_of_group',
                                limit_choices_to={'role': 'user'},
                                on_delete=models.SET_NULL,
                                null=True,
                                blank=True
                                )
    students = models.ManyToManyField(to=User, verbose_name='Ученики',
                                      limit_choices_to={'role': 'user'},
                                      related_name='students_of_group',
                                      blank=True
                                      )

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"


    def __str__(self):
        return self.name


class Lesson(models.Model):
    number = models.PositiveIntegerField(verbose_name='Номер урока', null=True, blank=True)
    lesson_name = models.CharField(verbose_name='Название урока',
                                   max_length=255,
                                   null=True,
                                   blank=True)
    description = models.TextField(verbose_name='Информация',
                                   max_length=5000,
                                   null=True,
                                   blank=True
                                   )
    video = models.URLField(verbose_name='Ссылка на запись урока',
                            max_length=200,
                            null=True,
                            blank=True
                            )
    course = models.ForeignKey(to=Course, 
                               verbose_name='Курс', 
                               related_name='related_course',
                               on_delete=models.SET_NULL, 
                               null=True, 
                               blank=True
                               )
    lesson_type = models.CharField(verbose_name='Бесплатный/платный',
                                   max_length=4,
                                   choices=LessonTypeChoices,
                                   default=LessonTypeChoices.FREE
                                   )

    def __str__(self):
        return self.lesson_name

    def is_accessible_by(self, user):

        if self.lesson_type == LessonTypeChoices.FREE:
            return True
        if self.course.is_paid_by(user):
            return True
        return False

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Урок'


class LessonPerGroup(models.Model):
    group = models.ForeignKey(to=Group,
                               verbose_name='Группа',
                               related_name='group_lesson',
                               on_delete=models.SET_NULL,
                               null=True,
                               blank=True
                               )
    lesson = models.ForeignKey(verbose_name='Урок',
                               to=Lesson,
                               related_name='lesson_group',
                               on_delete=models.CASCADE
                               )
    datetime = models.DateTimeField(verbose_name='Дата и время')

    def __str__(self):
        return f'Lesson conducted in {self.group.name} on {self.datetime}'

    class Meta:
            verbose_name = "Урок у группы"
            verbose_name_plural = "Уроки у групп"


class Visit(models.Model):
    is_currently_viewing = models.CharField(verbose_name='Посещение', max_length=15, choices=LessonVisitChoices,
                                            blank=True, default='')
    visit_date = models.DateTimeField(verbose_name='Дата посеения',
                                      auto_now_add=True
                                      )
    students = models.ForeignKey(verbose_name='Студент',
                                 to=User,
                                 limit_choices_to={'role': 'user'},
                                 related_name='students',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 blank=True
                                 )
    lesson = models.ForeignKey(verbose_name='Урок у группы',
                               to=LessonPerGroup,
                               related_name='visits', 
                               on_delete=models.CASCADE
                               )
    grade = models.CharField(verbose_name='Оценка', max_length=5, choices=VisitRateChoices, blank=True, default='')

    def __str__(self):
        return f'Visit by {self.students} on {self.visit_date}'

    class Meta:
        verbose_name = "Посещения"
        verbose_name_plural = "Посещения"
