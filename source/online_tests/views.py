import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.generic import View
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import OnlineTest, Question, UserTest
from .serializers import TestSerializer


class TestPassingView(LoginRequiredMixin, View):
    def get(self, request, test_id):
        test = OnlineTest.objects.get(id=test_id)
        questions = Question.objects.filter(test=test)
        context = {
            'test': test,
            'questions': questions,
            'countdown_seconds': test.countdown.total_seconds(),
        }
        return render(request, 'course_tests/test_passing.html', context)


class TestDetailView(APIView):
    serializer_class = TestSerializer

    def get(self, request, *args, **kwargs):
        test_id = self.kwargs['test_id']
        test = OnlineTest.objects.get(id=test_id)
        serializer = self.serializer_class(test)
        return Response(serializer.data)


@require_http_methods(["POST"])
def submit(request, test_id):
    test = get_object_or_404(OnlineTest, id=test_id)
    user = request.user
    user_test, created = UserTest.objects.get_or_create(user=user, test=test)
    correct_questions_count = 0

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid data format"}, status=400)

    questions = Question.objects.filter(test=test).prefetch_related(
        Prefetch('answers', to_attr='related_answers'),
    )

    for question in questions:
        user_answers = data.get(str(question.id), [])
        if user_answers:
            correct_flag = any(answer.is_correct and answer.id in user_answers for answer in question.related_answers)
            correct_questions_count += correct_flag

    total_questions_count = questions.count()
    incorrect_questions_count = total_questions_count - correct_questions_count
    user_test.correct_answer_count = correct_questions_count
    user_test.incorrect_answer_cnt = incorrect_questions_count
    user_test.save()

    print(f'Правильных ответов:{correct_questions_count}')
    print(f'Неправильных ответов:{incorrect_questions_count}')

    return JsonResponse({"result": "success"})

