from django.db import transaction
from django.shortcuts import render
from django.views.generic import ListView
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Test, Question, UserTest, UserAnswer
from .serializers import TestSerializer, UserTestSerializer, UserAnswerSerializer


def take_test(request, test_id):
    test = Test.objects.get(id=test_id)
    questions = Question.objects.filter(test=test)
    return render(request, 'tests/take_test.html', {'test': test, 'questions': questions})


class TestListView(ListView):
    model = Test
    template_name = '...'


class TestDetailView(generics.RetrieveAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer


class AnswerCreateView(APIView):
    def post(self, request):
        serializer = UserAnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserTestResultsView(generics.ListAPIView):
    serializer_class = UserTestSerializer

    def get_queryset(self):
        user = self.request.user
        return UserTest.objects.filter(user=user)


class TestSubmitView(APIView):
    @transaction.atomic
    def post(self, request):
        user_test_data = request.data.get('userTest')
        user_answers_data = request.data.get('userAnswers')

        user_test_serializer = UserTestSerializer(data=user_test_data)
        user_test_serializer.is_valid(raise_exception=True)
        user_test = user_test_serializer.save()

        UserAnswer.objects.filter(user_test__user=user_test.user, user_test__test=user_test.test).delete()

        user_answers = []
        for user_answer_data in user_answers_data:
            user_answer_serializer = UserAnswerSerializer(data=user_answer_data)
            user_answer_serializer.is_valid(raise_exception=True)
            user_answer = user_answer_serializer.save(user_test=user_test)
            user_answers.append(user_answer)

        user_test.update_answer_counts()

        return Response(UserTestSerializer(user_test).data, status=status.HTTP_201_CREATED)
