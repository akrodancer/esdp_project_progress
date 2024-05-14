from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from courses.models import Visit, Lesson, Course, CourseGroup, LessonPerGroup
from online_tests.models import OnlineTest, Question
from .account_type_choices import AccoutTypeChoices
from .user_queryset import CustomUserManager
from courses import AvatarUpload
from django.contrib.auth.models import UserManager
    

class User(AbstractUser):
    avatar = models.ImageField(verbose_name='Аватар', upload_to=AvatarUpload._upload, null=True, blank=True)
    email = models.EmailField(verbose_name='Электронная почта', unique=True)
    phone = models.CharField(verbose_name='Номер телефона', max_length=20)
    role = models.CharField(verbose_name='Должность', 
                            max_length=30, 
                            choices=AccoutTypeChoices,
                            default=AccoutTypeChoices.USER
                            )
    
    object = UserManager()
    user_set = CustomUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    def save(self, *args, **kwargs):
        if self.role == AccoutTypeChoices.TEACHER:
            self.is_staff = True
        else:
            self.is_staff = False
        super().save(*args, **kwargs)
        models_to_manage = [Course, OnlineTest, Lesson, Visit, Question, OnlineTest, CourseGroup, LessonPerGroup]
        if self.role == AccoutTypeChoices.TEACHER:
            for model_class in models_to_manage:
                content_type = ContentType.objects.get_for_model(model_class)
                permissions = Permission.objects.filter(content_type=content_type)
                self.user_permissions.add(*permissions)
    
    class Meta:
        verbose_name='Пользователи'
        verbose_name_plural = 'Пользователи'


class Comment(models.Model):
    content = models.TextField(verbose_name='Содержание')
    teacher = models.ForeignKey(to=User, verbose_name='Учитель', limit_choices_to={'role': 'teacher'}, related_name='comments_given', on_delete=models.CASCADE)
    student = models.ForeignKey(to=User, verbose_name='Ученик', limit_choices_to={'role': 'user'}, related_name='comments_received', on_delete=models.CASCADE)
    course = models.ForeignKey(to=Course, verbose_name='Курс ученика', related_name='comments', on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(verbose_name='Время публикации', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Время редактирования', auto_now=True)
    
    class Meta:
        verbose_name='Комментарии'
        verbose_name_plural='Комментарии'


class SignedUpUsers(models.Model):
    first_name = models.CharField(verbose_name='Имя')
    last_name = models.CharField(verbose_name='Фамилия')
    phone = models.CharField(verbose_name='Телефон')
    email = models.EmailField(verbose_name='Электронная почта')
    course = models.CharField(verbose_name='Курс')
    
    def __str__(self) -> str:
        return f'{self.first_name}, {self.last_name}'
    
    class Meta:
        verbose_name='Заявки на курсы'
        verbose_name_plural='Заявки на курсы'