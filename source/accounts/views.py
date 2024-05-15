from typing import Any
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.views.generic import CreateView, DetailView, ListView, View, DeleteView, UpdateView
from django_filters.views import FilterView
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse, reverse_lazy
from courses.models import Visit, Course, CourseGroup
from .models import Comment
from .json_form_handler import JsonFormHandler
from .forms import NewUserForm, LoginUserForm, CommentForm, SignedUpUsersForm
from .filters import StudentFilter
from django.core.exceptions import PermissionDenied
from .account_type_choices import AccoutTypeChoices
from courses.lesson_choices import LessonVisitChoices

def logout_view(request):
    logout(request)
    return redirect('courses:index')


class UserLogin(View):
    def post(self, request, *args, **kwargs):
        form = LoginUserForm(request.POST)
        try:
            current_user = authenticate(request, 
                                        username=form['username'].value(),
                                        password=form['password'].value())
            login(request, current_user)
        except:
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


class StudentListView(FilterView, ListView):
    template_name = 'accounts/student_list.html'
    model = get_user_model()
    filterset_class = StudentFilter
    context_object_name = 'students'

    def get_queryset(self):
        queryset = get_user_model().objects.none()
        return queryset


class StudentDetailView(DetailView):
    model = get_user_model()
    template_name = 'accounts/student_detail.html'
    context_object_name = 'student'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.role != AccoutTypeChoices.USER:
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
                             'is_currently_viewing': True if visit.is_currently_viewing==LessonVisitChoices.IN else False,
                             'student': visit.students.id,
                             'course': visit.lesson.lesson.course.id,
                             }
                            for visit in visits])
            try:
                group = student.students_of_group.get(course=selected_course)
                context['group'] = group
            except:
                context['group'] = ''
            comments = Comment.objects.filter(student__id=student_id, course__id=course_id).order_by('-created_at')
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
        return self.request.user.role == AccoutTypeChoices.TEACHER

    def form_valid(self, form):
        student = get_object_or_404(get_user_model(), pk=self.kwargs.get('pk'))
        course_id = self.request.GET.get('course', '')
        course = get_object_or_404(Course, pk=course_id)
        comment = form.save(commit=False)
        comment.student = student
        comment.teacher = self.request.user
        comment.course = course
        comment.save()
        url = reverse('accounts:student_detail', kwargs={'pk': student.pk}) + f'?course={course_id}'
        return HttpResponseRedirect(url)


class CommentDeleteView(UserPassesTestMixin, DeleteView):
    model = Comment

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.teacher

    def get_success_url(self):
        course_id = self.request.GET.get('course', '')
        return reverse_lazy('accounts:student_detail', kwargs={'pk': self.object.student.pk}) + f'?course={course_id}'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.get_success_url())


class CommentUpdateView(UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.teacher

    def get_success_url(self):
        course_id = self.request.GET.get('course', '')
        return reverse_lazy('accounts:student_detail', kwargs={'pk': self.object.student.pk}) + f'?course={course_id}'

    def form_valid(self, form):
        return super().form_valid(form)


class SignUpUsersView(View):
    def post(self, request, *args, **kwargs):
        record = JsonFormHandler(request=self.request, 
                                form=SignedUpUsersForm)
        record.create_object()
        
        return record.response()