from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import redirect, reverse, get_object_or_404
from django.contrib.auth import login, get_user_model
from django.views.generic import CreateView, DetailView, UpdateView, ListView, View, FormView
from django.contrib.auth.mixins import UserPassesTestMixin
from accounts.forms import CommentForm
from django.contrib.auth.views import PasswordChangeView
from courses.models import Course, Visit, Lesson
from accounts.models import Comment, User

# Create your views here.


class StudentListView(ListView):
    template_name = 'student_list.html'
    model = get_user_model()
    context_object_name = 'students'

    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', None)
        if search_query:
            name_parts = search_query.split(' ')
            if len(name_parts) >= 2:
                queryset = queryset.filter(
                    Q(first_name__iexact=name_parts[0]) | Q(last_name__iexact=name_parts[1]),
                    role='user'
                )
            else:
                queryset = queryset.filter(
                    Q(first_name__iexact=search_query) | Q(last_name__iexact=search_query),
                    role='user'
                )
        else:
            queryset = queryset.none()
        return queryset


class StudentDetailView(DetailView):
    model = get_user_model()
    template_name = 'student_detail.html'
    context_object_name = 'student'

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
        student = get_object_or_404(User, pk=self.kwargs.get('pk'))
        comment = form.save(commit=False)
        comment.student = student
        comment.teacher = self.request.user
        comment.save()
        course_id = self.request.GET.get('course', '')
        url = reverse('accounts:student_detail', kwargs={'pk': student.pk}) + f'?course={course_id}'
        return HttpResponseRedirect(url)
