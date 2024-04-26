from django.contrib import admin
from django.db import transaction
from courses.models import Course, Lesson, Visit, LessonPerGroup, Group, Lesson

class VisitInline(admin.TabularInline):
    model = Visit
    fields = ('students', 'is_currently_viewing', 'grade')
    extra = 0  # чтобы не создавать по умолчанию пустые строки

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 0
    fields = ('number', 'lesson_name', 'description',
              'video', 'course', 'lesson_type')
    fk_name = 'course'
    show_change_link = True


@admin.register(Course)
class CustomCourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline]
    list_display = (
        'course_name',
        'date_start',
        'date_finish',
    )
    fields = ('course_name', 'description', 'date_start',
              'course_image', 'date_finish', 'teacher',
              'students', 'paid_by')


@admin.register(Group)
class CustomGroupAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )
    fields = ('name', 'teacher', 'students')

@admin.register(LessonPerGroup)
class LessonPerGroupAdmin(admin.ModelAdmin):
    inlines = [VisitInline]
    list_display = ['lesson']

    @transaction.atomic
    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)
        lesson = form.instance
        students = lesson.group.students.all()
        for student in students:
            Visit.objects.get_or_create(students=student, lesson=lesson)
