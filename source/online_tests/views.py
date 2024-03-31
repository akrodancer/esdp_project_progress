import datetime
import json
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.generic import View, TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import OnlineTest, Question, UserTest, Answer
from .serializers import TestSerializer


class AllTestsView(TemplateView):
    template_name = 'course_tests/tests_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        language = self.request.GET.get('language')
        tests = OnlineTest.objects.all()
        if language == 'RU':
            context['tests'] = tests.filter(test_language='русский')
        elif language == 'KG':
            context['tests'] = tests.filter(test_language='кыргызский')
        else:
            context['tests'] = tests.all()
        return context


class TestView(LoginRequiredMixin, View):
    template_name = 'course_tests/test_start.html'

    def get(self, request, test_id):
        test = get_object_or_404(OnlineTest, id=test_id)
        questions_count = Question.objects.filter(test=test).count()
        total_minutes = int(test.countdown.total_seconds() // 60)
        context = {
            'test': test,
            'questions_count': questions_count,
            'total_minutes': total_minutes
        }
        return render(request, self.template_name, context)


class TestPassingView(LoginRequiredMixin, View):
    def get(self, request, test_id):
        test = get_object_or_404(OnlineTest, id=test_id)
        user = request.user
        user_test, created = UserTest.objects.get_or_create(user=user, test=test)
        user_test.test_start = timezone.now()
        user_test.save()
        answers = []

        questions = Question.objects.filter(test=test)
        for question in questions:
            question_answers = Answer.objects.filter(question_id=question.pk)
            answers = question_answers

        server_time = datetime.datetime.now()
        context = {
            'test': test,
            'questions': questions,
            'countdown_seconds': test.countdown.total_seconds(),
            'answers': answers,
            'server_time': server_time.strftime('%Y-%m-%dT%H:%M:%S'),
            'minutes': test.countdown.seconds // 60
        }
        return render(request, 'course_tests/test_passing.html', context)


class TestDetailView(APIView):
    serializer_class = TestSerializer

    def get(self, request, *args, **kwargs):
        test_id = self.kwargs['test_id']
        test = get_object_or_404(OnlineTest, id=test_id)
        serializer = self.serializer_class(test)
        return Response(serializer.data)


class TestSubmitView(View):
    @staticmethod
    def process_user_answers(request_body, test):
        try:
            data = json.loads(request_body)
        except json.JSONDecodeError:
            raise JsonResponse({"error": "Invalid data format"}, status=400)

        correct_count = 0
        incorrect_count = 0

        questions = Question.objects.filter(test=test).prefetch_related(
            Prefetch('answers', to_attr='related_answers'),
        )

        for question in questions:
            user_answers = data.get(str(question.id), [])
            if user_answers:
                correct_flag = any(
                    answer.is_correct and answer.id in user_answers for answer in question.related_answers)
                if correct_flag:
                    correct_count += 1
                else:
                    incorrect_count += 1
            else:
                incorrect_count += 1

        return correct_count, incorrect_count

    @staticmethod
    def save_test_results(user_test, correct_count, incorrect_count):
        user_test.correct_answer_count = correct_count
        user_test.incorrect_answer_cnt = incorrect_count
        user_test.attempts += 1
        user_test.save()
        return user_test

    @staticmethod
    def post(request, test_id):
        test = get_object_or_404(OnlineTest, id=test_id)
        user = request.user
        correct_count, incorrect_count = TestSubmitView.process_user_answers(request.body, test)
        user_test = UserTest.objects.get(user=user, test=test)
        TestSubmitView.save_test_results(user_test, correct_count, incorrect_count)
        return JsonResponse({"user_test_id": user_test.id})


def test_results(request, user_test_id):
    user_test = get_object_or_404(UserTest, id=user_test_id)
    total_questions_count = user_test.correct_answer_count + user_test.incorrect_answer_cnt

    if total_questions_count > 0:
        progress = int((user_test.correct_answer_count / total_questions_count) * 100)
    else:
        progress = 0

    time_spent = user_test.test_end - user_test.test_start
    time_spent_seconds = time_spent.total_seconds()
    time_spent_format = (f"{int(time_spent_seconds // 3600):02d}:"
                         f"{int((time_spent_seconds % 3600) // 60):02d}:{int(time_spent_seconds):02d}")

    context = {
        'test_name': user_test.test.test_name,
        'user_test': user_test,
        'progress': progress,
        'total_questions_count': total_questions_count,
        'test_id': user_test.test.id,
        'time_spent': time_spent_format,
    }

    return render(request, 'course_tests/test_results.html', context)
