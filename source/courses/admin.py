from django.contrib import admin

from courses.models import Course, Lesson


# Register your models here.
class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 0
    fields = ('lesson_name', 'grade', 'description',
                'video', 'datetime', 'course','lesson_type')
    fk_name = 'course'


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
