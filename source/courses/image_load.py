import os
import uuid

from django.conf import settings


class ImageDirs:
    MEDIA = 'media/'
    AVATAR_DIR = MEDIA + 'avatars'
    COURSE_DIR = MEDIA + 'courses'
    ANSWER_DIR = MEDIA + 'answers'
    QUESTION_DIR = MEDIA + 'questions'
    HOME_DIR = MEDIA + 'home_images'


class ImageUpload:
    @staticmethod
    def _upload(instance, filename):
        pass


class AvatarUpload(ImageUpload):
    @staticmethod
    def _upload(instance, filename):
        extension = filename.split('.')[-1]
        unique_filename = f'{uuid.uuid4()}.{extension}'
        return os.path.join(ImageDirs.AVATAR_DIR, unique_filename)


class CourseUpload(ImageUpload):
    @staticmethod
    def _upload(instance, filename):
        extension = filename.split('.')[-1]
        unique_filename = f'{uuid.uuid4()}.{extension}'
        return os.path.join(ImageDirs.COURSE_DIR, unique_filename)


class AnswerUpload(ImageUpload):
    @staticmethod
    def _upload(instance, filename):
        extension = filename.split('.')[-1]
        unique_filename = f'{uuid.uuid4()}.{extension}'
        return os.path.join(ImageDirs.ANSWER_DIR, unique_filename)


class QuestionUpload(ImageUpload):
    @staticmethod
    def _upload(instance, filename):
        extension = filename.split('.')[-1]
        unique_filename = f'{uuid.uuid4()}.{extension}'
        return os.path.join(ImageDirs.QUESTION_DIR, unique_filename)
    
class HomeUpload(ImageUpload):
    @staticmethod
    def _upload(instance, filename):
        extension = filename.split('.')[-1]
        unique_filename = f'{uuid.uuid4()}.{extension}'
        return os.path.join(ImageDirs.HOME_DIR, unique_filename)
