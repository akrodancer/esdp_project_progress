from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from accounts.models import User, Comment
from courses.models import Visit, Lesson


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

        comment_permissions = {
            'add_comment': 'Can add comment',
            'change_comment': 'Can change comment',
            'delete_comment': 'Can delete comment',
            'view_comment': 'Can view comment',
        }
        assign_permissions_for_model(Comment, comment_permissions)

        visit_permissions = {
            'add_visit': 'Can add visit',
            'change_visit': 'Can change visit',
            'delete_visit': 'Can delete visit',
            'view_visit': 'Can view visit',
        }
        assign_permissions_for_model(Visit, visit_permissions)

        lesson_permissions = {
            'add_lesson': 'Can add lesson',
            'change_lesson': 'Can change lesson',
            'delete_lesson': 'Can delete lesson',
            'view_lesson': 'Can view lesson',
        }
        assign_permissions_for_model(Lesson, lesson_permissions)

        self.stdout.write(self.style.SUCCESS(
            f"Разрешения выданы"
        ))
