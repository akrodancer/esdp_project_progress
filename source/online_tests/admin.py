from django.contrib import admin
from .models import Test, Question, Answer, UserTest, UserAnswer



class AnswerInline(admin.StackedInline):
    model = Answer
    extra = 0
    fields = ('answer_text', 'answer_image', 'is_correct')
    fk_name = 'question'

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 0
    fields = ('question_name', 'question_text', 'question_image')
    fk_name = 'test'


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['id', 'test_name']

# @admin.register(Question)
# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ['id', 'question_name', 'question_text']

# @admin.register(Answer)
# class AnswerAdmin(admin.ModelAdmin):
#     list_display = ['id', 'is_correct', 'answer_text']

# @admin.register(UserTest)
# class UserTestAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user', 'test', 'date_taken']

# @admin.register(UserAnswer)
# class UserAnswerAdmin(admin.ModelAdmin):
#     list_display = ['id', 'user_test', 'question', 'answer']