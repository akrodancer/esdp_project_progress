from django.db import models
from .account_type_choices import AccoutTypeChoices


class UserQueryset(models.QuerySet):
    def get_teachers(self):
        return self.filter(role=AccoutTypeChoices.TEACHER)

    def get_students(self):
        return self.filter(role=AccoutTypeChoices.USER)
    
    def by_username(self, username):
        try:
            return self.get(username=username)
        except:
            return None
    
    
class CustomUserManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return UserQueryset(self.model)
    
    def get_teachers(self):
        return self.get_queryset().get_teachers()
    
    def get_students(self):
        return self.get_queryset().get_students()
    
    def by_username(self, username):
        return self.get_queryset().by_username(username=username)