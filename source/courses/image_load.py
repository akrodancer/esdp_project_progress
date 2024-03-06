import os
import uuid

from django.conf import settings


class ImageDirs:
    AVATAR_DIR = os.path.join(settings.MEDIA_ROOT, 'avatars')
    COURSE_DIR = os.path.join(settings.MEDIA_ROOT, 'courses')
    ANSWER_DIR = os.path.join(settings.MEDIA_ROOT, 'answers')
    QUESTION_DIR = os.path.join(settings.MEDIA_ROOT, 'questions')


class ImageUpload:
    @staticmethod
    def _upload(instance, filename):
        pass


class AvatarUpload(ImageUpload):
    @staticmethod
    def _upload(instance, filename):
        extension = filename.split('.')[-1]
        unique_filename = f'{uuid.uuid4()}.{extension}'
        return os.path.join('avatars', unique_filename)


class CourseUpload(ImageUpload):
    @staticmethod
    def _upload(instance, filename):
        extension = filename.split('.')[-1]
        unique_filename = f'{uuid.uuid4()}.{extension}'
        return os.path.join('courses', unique_filename)


class AnswerUpload(ImageUpload):
    @staticmethod
    def _upload(instance, filename):
        extension = filename.split('.')[-1]
        unique_filename = f'{uuid.uuid4()}.{extension}'
        return os.path.join('answers', unique_filename)


class QuestionUpload(ImageUpload):
    @staticmethod
    def _upload(instance, filename):
        extension = filename.split('.')[-1]
        unique_filename = f'{uuid.uuid4()}.{extension}'
        return os.path.join('questions', unique_filename)
