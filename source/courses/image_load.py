import uuid
import os
from django.conf import settings




class ImageDirs:
    AVATAR_DIR = os.path.join(settings.MEDIA_DIR, 'avatars')
    COURSE_DIR = os.path.join(settings.MEDIA_DIR, 'courses')
    ANSWER_DIR = os.path.join(settings.MEDIA_DIR, 'answers')
    QUESTION_DIR = os.path.join(settings.MEDIA_DIR, 'questions')



class ImageUpload:
    def _upload(instance, filename):
        pass

class AvatarUpload(ImageUpload):
    @staticmethod
    def _upload(instance, filename):
        extension = filename.split('.')[-1]  
        url = ImageDirs.AVATAR_DIR + f'/{uuid.uuid4()}.{extension}'
        return url
    
class CourseUpload(ImageUpload):
    @staticmethod
    def _upload(instance, filename):
        extension = filename.split('.')[-1]  
        url = ImageDirs.COURSE_DIR + f'/{uuid.uuid4()}.{extension}'
        return url
    
class AnswerUpload(ImageUpload):
    @staticmethod
    def _upload(instance, filename):
        extension = filename.split('.')[-1]  
        url = ImageDirs.ANSWER_DIR + f'/{uuid.uuid4()}.{extension}'
        return url
    
class QuestionUpload(ImageUpload):
    @staticmethod
    def _upload(instance, filename):
        extension = filename.split('.')[-1]  
        url = ImageDirs.QUESTION_DIR + f'/{uuid.uuid4()}.{extension}'
        return url
    
