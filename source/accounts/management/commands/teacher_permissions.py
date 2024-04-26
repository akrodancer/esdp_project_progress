from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import User, Comment
from courses.models import Visit, Lesson, Course, Group, LessonPerGroup
from online_tests.models import OnlineTest, Question


class Command(BaseCommand):
    help = 'Выдает разрешения и is_staff пользователям с ролью teacher'

    def handle(self, *args, **options):
        def assign_permissions_for_model(model_class, permissions):
            content_type = ContentType.objects.get_for_model(model_class)
            for codename, name in permissions.items():
                permission, _ = Permission.objects.get_or_create(
                    codename=codename,
                    content_type=content_type,
                    defaults={'name': name}
                )
                for teacher in teachers:
                    teacher.user_permissions.add(permission)
                    teacher.is_staff = True
                    teacher.save()

        teachers = User.objects.filter(role='teacher')

        models_to_manage = [Course, OnlineTest, Lesson, Visit, Question, OnlineTest, Group, LessonPerGroup]

        permissions_mapping = {
            Course: {
                'add_course': 'Can add course',
                'change_course': 'Can change course',
                'delete_course': 'Can delete course',
                'view_course': 'Can view course',
            },
            Lesson: {
                'add_lesson': 'Can add lesson',
                'change_lesson': 'Can change lesson',
                'delete_lesson': 'Can delete lesson',
                'view_lesson': 'Can view lesson',
            },
            Visit: {
                'add_visit': 'Can add visit',
                'change_visit': 'Can change visit',
                'delete_visit': 'Can delete visit',
                'view_visit': 'Can view visit',
            },
            Question: {
                'add_question': 'Can add question',
                'change_question': 'Can change question',
                'delete_question': 'Can delete question',
                'view_question': 'Can view question',
            },
            OnlineTest: {
                'add_onlinetest': 'Can add online test',
                'change_onlinetest': 'Can change online test',
                'delete_onlinetest': 'Can delete online test',
                'view_onlinetest': 'Can view online test',
            },
            Group: {
                'add_group': 'Can add group',
                'change_group': 'Can change group',
                'delete_group': 'Can delete group',
                'view_group': 'Can view group',
            },
            LessonPerGroup: {
                'add_lessonpergroup': 'Can add lesson per group',
                'change_lessonpergroup': 'Can change lesson per group',
                'delete_lessonpergroup': 'Can delete lesson per group',
                'view_lessonpergroup': 'Can view lesson per group',
            }
        }

        # Применение разрешений для каждой модели
        for model_class in models_to_manage:
            if model_class in permissions_mapping:
                assign_permissions_for_model(model_class, permissions_mapping[model_class])

        self.stdout.write(self.style.SUCCESS(
            f"Разрешения выданы"
        ))
