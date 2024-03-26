from django.contrib import admin

from .models import OnlineTest, Question, Answer


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
    show_change_link = True


@admin.register(OnlineTest)
class TestAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]
    list_display = ['id', 'test_name']


@admin.register(Question)
class QuestionAdminAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]
    list_display = ['id', 'question_name']
