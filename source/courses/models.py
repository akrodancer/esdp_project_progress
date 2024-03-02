from django.db import models
from courses.lesson_types import LESSON_TYPES
from accounts.models import User
from . import CourseUpload


class Course(models.Model):
    class Meta:
        verbose_name = "Курсы"
        verbose_name_plural = "Курсы"

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

    def __str__(self):
        return self.course_name

    def is_paid_by(self, user):
        return self.paid_by.filter(pk=user.pk).exists()


class Lesson(models.Model):
    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Урок'


    lesson_name = models.CharField(verbose_name='Название урока',
                                    max_length=255, 
                                    null=True, 
                                    blank=True)
    grade = models.PositiveIntegerField(verbose_name='Уровень')
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
    datetime = models.DateTimeField(verbose_name='Дата и время', )
    course = models.ForeignKey(to=Course, verbose_name='Курс', 
                               related_name='lessons', 
                               on_delete=models.SET_NULL, 
                               null=True, 
                               blank=True
                               )
    lesson_type = models.CharField(verbose_name='Бесплатный/платный',
                                    max_length=4, 
                                   choices=LESSON_TYPES, 
                                   default=LESSON_TYPES.FREE
                                   )

    def __str__(self):
        return self.lesson_name

    def is_accessible_by(self, user):

        if self.lesson_type == 'free':
            return True
        if self.course.is_paid_by(user):
            return True
        return False


class Visit(models.Model):
    class Meta:
        verbose_name = "Посещения"
        verbose_name_plural = "Посещения"

    is_currently_viewing = models.BooleanField()
    visit_date = models.DateTimeField(auto_now_add=True)
    students = models.ForeignKey(to=User, limit_choices_to={'role', 'user'}, related_name='visits',
                                 on_delete=models.SET_NULL, null=True, blank=True)
    lesson = models.ForeignKey(to=Lesson, related_name='visits', on_delete=models.CASCADE)

    def __str__(self):
        return f'Visit by {self.students} on {self.visit_date}'


