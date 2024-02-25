from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from accounts.models import User
from courses.models import Course


class IndexPageView(TemplateView):
    template_name = 'courses/index.html'


class AboutUsView(ListView):
    model = User
    template_name = 'courses/about_us.html'
    context_object_name = 'teachers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['teachers'] = User.objects.all().filter(role='teacher')
        return context


class CoursesView(ListView):
    model = Course
    template_name = 'courses/courses_view.html'
    context_object_name = 'courses'
