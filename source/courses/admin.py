from django.contrib import admin
from django import forms
from courses.models import Course, Lesson, Visit, LessonPerGroup, CourseGroup, Lesson


class ParentFormSet(forms.BaseInlineFormSet):
    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs['parent_object'] = self.instance
        return kwargs

class LessonPerGroupForm(forms.ModelForm):
    def __init__(self, *args, parent_object, **kwargs):
        self.parent_object = parent_object
        super().__init__(*args, **kwargs)
        current_group = self.parent_object
        course = current_group.course
        self.fields['lesson'].queryset = Lesson.objects.filter(course=course)

class PeopleForGroupFormset(forms.ModelForm):
    def __init__(self, *args, parent_object, **kwargs):
        self.parent_object = parent_object
        super().__init__(*args, **kwargs)
        current_course = self.parent_object
        try:
            self.fields['teacher'].queryset = current_course.teacher.all()
            self.fields['students'].queryset = current_course.students.all()
        except ValueError:
            pass

class StudentsForGroupFormset(forms.ModelForm):
    def __init__(self, *args, parent_object, **kwargs):
        self.parent_object = parent_object
        super().__init__(*args, **kwargs)
        current_course = self.parent_object.group
        try:
            self.fields['students'].queryset = current_course.students.all()
        except ValueError:
            pass
             

class VisitInline(admin.TabularInline):
    model = Visit
    fields = ('students', 'is_currently_viewing', 'grade')
    extra = 0
    fk_name = 'lesson'  
    form = StudentsForGroupFormset
    formset = ParentFormSet

class LessonInline(admin.StackedInline):
    model = Lesson
    extra = 0
    fields = ('number', 'lesson_name', 'description',
              'video', 'course', 'lesson_type')
    fk_name = 'course'
    show_change_link = True


class LessonPerGroupInline(admin.StackedInline):
    model = LessonPerGroup
    extra = 0
    fk_name = 'group'
    show_change_link = True
    form = LessonPerGroupForm
    formset = ParentFormSet


class GroupInline(admin.StackedInline):
    model = CourseGroup
    extra = 0
    fields = ('name', 'teacher', 'students')
    fk_name = 'course'
    show_change_link = True
    form = PeopleForGroupFormset
    formset = ParentFormSet

@admin.register(Course)
class CustomCourseAdmin(admin.ModelAdmin):
    inlines = [LessonInline, GroupInline]
    list_display = (
        'course_name',
        'date_start',
        'date_finish',
    )
    fields = ('course_name', 'description', 'date_start',
              'course_image', 'date_finish', 'teacher',
              'students')


@admin.register(CourseGroup)
class CustomGroupAdmin(admin.ModelAdmin):
    inlines = [LessonPerGroupInline]
    list_display = ('name',)
    fields = ('name', 
              'teacher', 
              'students')


@admin.register(LessonPerGroup)
class LessonPerGroupAdmin(admin.ModelAdmin):
    inlines = [VisitInline]
    list_display = ['lesson']
    get_model_perms = lambda self, req: {}