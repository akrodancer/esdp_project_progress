from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import TemplateView, View
from accounts.models import User
from courses.models import Course
from accounts.forms import NewUserForm, LoginUserForm


class IndexPageView(View):
    def get(self, request, *args, **kwargs):
        template_name = 'courses/index.html'
        login_form = LoginUserForm
        context = {
            'login_form': login_form
            }

        return render(request, template_name, context)
    

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
