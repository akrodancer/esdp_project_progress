from django.contrib import admin
from .models import Test, Question, Answer, UserTest, UserAnswer

@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ['id', 'test_name']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'question_name', 'question_text']

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'is_correct', 'answer_text']

@admin.register(UserTest)
class UserTestAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'test', 'date_taken']

@admin.register(UserAnswer)
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_test', 'question', 'answer']