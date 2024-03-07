from typing import Any
from django.db.models import Q
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.views.generic import CreateView, DetailView, ListView, View
from django.shortcuts import redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import CommentForm, SignedUpUsersForm
from .models import Comment
from .forms import NewUserForm, LoginUserForm
from .json_form_handler import JsonFormHandler
from courses.models import Visit, Course

def logout_view(request):
    logout(request)
    return redirect('courses:index')


class UserLogin(View):
    def post(self, request, *args, **kwargs):
        form = LoginUserForm(request.POST)
        if form.is_valid():
            current_user = authenticate(request, 
                                    username=form['username'].value(),
                                    password=form['password'].value())
            login(request, current_user)
            return HttpResponseRedirect(self.get_success_url())
        else:
            messages.error(request, 'Неверный логин или пароль')
            return HttpResponseRedirect(self.get_success_url())
            
    def get_success_url(self):
        next_url = self.request.POST.get('next')
        if not next_url:
            next_url = reverse('courses:index')
        return next_url


class UserRegisterView(CreateView):
    model = get_user_model()
    template_name = 'accounts/registration.html'
    form_class = NewUserForm

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse('courses:index'))


class StudentListView(ListView):
    template_name = 'accounts/student_list.html'
    model = get_user_model()
    context_object_name = 'students'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', None)
        if search_query:
            name_parts = search_query.split(' ')
            if len(name_parts) >= 2:
                queryset = queryset.filter(
                    Q(first_name__iexact=name_parts[0]) & Q(last_name__iexact=name_parts[1]),
                    role='user'
                )
            else:
                queryset = queryset.none()
        else:
            queryset = queryset.none()
        return queryset


class StudentDetailView(DetailView):
    model = get_user_model()
    template_name = 'accounts/student_detail.html'
    context_object_name = 'student'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        student_id = self.kwargs['pk']
        course_id = self.request.GET.get('course')
        student = get_object_or_404(get_user_model(), pk=student_id)
        if course_id:
            selected_course = get_object_or_404(Course, id=course_id)
            teachers = selected_course.teacher.all()
            visits = Visit.objects.filter(students=student, lesson__course=selected_course)
            comments = Comment.objects.filter(student__id=student_id)
            context['teachers'] = teachers
            context['selected_course'] = selected_course
            context['visits'] = visits
            context['comment_form'] = CommentForm()
            context['comments'] = comments
            context['student'] = student
        return context

    def post(self, request, *args, **kwargs):
        student_id = self.kwargs['pk']
        student = get_object_or_404(get_user_model(), pk=student_id)
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            content = comment_form.cleaned_data['content']
            teacher = request.user
            Comment.objects.create(content=content, teacher=teacher, student=student)
        url = reverse('accounts:student_detail', kwargs={'pk': student_id})
        return HttpResponseRedirect(url)


class SignUpUsersView(View):
    def post(self, request, *args, **kwargs):
        record = JsonFormHandler(request=self.request, 
                                form=SignedUpUsersForm)
        record.create_object()
        
        return record.response()