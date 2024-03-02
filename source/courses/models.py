from django.db import models
from courses.lesson_types import LESSON_TYPES
from accounts.models import User


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
                                     upload_to='...', 
                                     null=True, 
                                     blank=True
                                     )
    teacher = models.ManyToManyField(User, verbose_name='Учители', 
                                     limit_choices_to={'role': 'teacher'}, 
                                     related_name='courses_taught'
                                     )
    students = models.ManyToManyField(User, verbose_name='Ученики', 
                                      limit_choices_to={'role': 'user'}, 
                                      related_name='enrolled_courses',
                                      blank=True
                                      )
    paid_by = models.ManyToManyField(User, verbose_name='Те, кто оплатил', 
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

<<<<<<< HEAD
    LESSON_TYPES = (
        ('free', 'Free'),
        ('paid', 'Paid'),
    )
<<<<<<< HEAD
    lesson_name = models.CharField(max_length=255)
    grade = models.PositiveIntegerField()
    description = models.TextField(max_length=5000)
    video = models.URLField(max_length=200, null=True)
    datetime = models.DateTimeField()
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.SET_NULL, null=True)
    lesson_type = models.CharField(max_length=4, choices=LESSON_TYPES, default='free')
=======
    lesson_name = models.CharField(verbose_name='Название урока', max_length=255, null=True, blank=True)
    grade = models.PositiveIntegerField(verbose_name='Уровень', )
    description = models.TextField(verbose_name='Информация', max_length=5000, null=True, blank=True)
    video = models.URLField(verbose_name='Ссылка на запись урока', max_length=200, null=True, blank=True)
    datetime = models.DateTimeField(verbose_name='Дата и время', )
    course = models.ForeignKey(Course, verbose_name='Курс', related_name='lessons', on_delete=models.CASCADE, null=True)
    lesson_type = models.CharField(verbose_name='Бесплатный/платный', max_length=4, choices=LESSON_TYPES, default='free')
>>>>>>> 2cbba32 ( #2 Добавлены конфиги для django-jet)
=======
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
    course = models.ForeignKey(Course, verbose_name='Курс', 
                               related_name='lessons', 
                               on_delete=models.SET_NULL, 
                               null=True, 
                               blank=True
                               )
    lesson_type = models.CharField(verbose_name='Бесплатный/платный',
                                    max_length=4, 
                                   choices=[x.value for x in LESSON_TYPES], 
                                   default=LESSON_TYPES.free.value
                                   )
>>>>>>> ec0f734 ( #3 Добавлены классы наследующие Enum для выборов)

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
    students = models.ForeignKey(User, limit_choices_to={'role', 'user'}, related_name='visits',
                                 on_delete=models.SET_NULL, null=True, blank=True)
    lesson = models.ForeignKey(Lesson, related_name='visits', on_delete=models.CASCADE)

    def __str__(self):
        return f'Visit by {self.students} on {self.visit_date}'


