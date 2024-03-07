from django.shortcuts import render, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.views.generic import CreateView, DetailView, ListView, UpdateView, View
from accounts.forms import NewUserForm, LoginUserForm
from typing import Any
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.shortcuts import redirect, reverse, get_object_or_404
from django.contrib.auth import login, get_user_model
from django.views.generic import CreateView, DetailView, UpdateView, ListView, View, FormView
from django.contrib.auth.mixins import UserPassesTestMixin
from accounts.forms import CommentForm
from accounts.models import Comment
from courses.models import Visit, Course
from django.contrib.auth.views import PasswordChangeView
from courses.models import Course, Visit, Lesson
from accounts.models import Comment, User
from django_filters.views import FilterView
from .filters import StudentFilter


# Create your views here.

def logout_view(request):
    logout(request)
    return redirect('courses:index')


class UserLogin(View):
    def post(self, request, *args, **kwargs):
        form = LoginUserForm(request.POST)
        current_user = authenticate(request,
                                    username=form['username'].value(),
                                    password=form['password'].value())
        if current_user:
            login(request, current_user)

        return redirect(reverse('courses:index'))

    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if not next_url:
            next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('courses:index')
        return next_url


class UserRegisterView(CreateView):
    model = User
    template_name = 'accounts/sign_up.html'
    form_class = NewUserForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse('courses:index'))


class StudentListView(FilterView, ListView):
    model = get_user_model()
    filterset_class = StudentFilter
    template_name = 'accounts/student_list.html'
    context_object_name = 'students'


class StudentDetailView(DetailView):
    model = get_user_model()
    template_name = 'accounts/student_detail.html'
    context_object_name = 'student'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.role != 'user':
            raise Http404('Страница не найдена')
        course_id = self.request.GET.get('course')
        if not course_id:
            raise Http404('Страница не найдена')
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs['pk']
        course_id = self.request.GET.get('course')
        student = get_object_or_404(get_user_model(), pk=student_id)
        if course_id:
            selected_course = get_object_or_404(Course, id=course_id)
            teachers = selected_course.teacher.all()
            visits = Visit.objects.all()
            visits_data = ([{'visit_date': visit.visit_date.isoformat(),
                             'is_currently_viewing': True if visit.is_currently_viewing else False,
                             'student': visit.students.id,
                             'course': visit.lesson.course.id,
                             }
                            for visit in visits])
            comments = Comment.objects.filter(student__id=student_id)
            context['filter'] = StudentFilter
            context['teachers'] = teachers
            context['selected_course'] = selected_course
            context['visits_data'] = visits_data
            context['comment_form'] = CommentForm()
            context['comments'] = comments
            context['student'] = student
        return context


class CommentCreateView(UserPassesTestMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'student_detail.html'

    def test_func(self):
        return self.request.user.role == 'teacher'

    def form_valid(self, form):
        student = get_object_or_404(get_user_model(), pk=self.kwargs.get('pk'))
        comment = form.save(commit=False)
        comment.student = student
        comment.teacher = self.request.user
        comment.save()
        course_id = self.request.GET.get('course', '')
        url = reverse('accounts:student_detail', kwargs={'pk': student.pk}) + f'?course={course_id}'
        return HttpResponseRedirect(url)


