from django.contrib.auth.decorators import login_required
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Test, UserTest, UserAnswer
from .serializers import TestSerializer


@login_required
def take_test(request, test_id):
    test = Test.objects.get(id=test_id)
    csrf_token = get_token(request)
    return render(request, 'course_test/test_passing.html',
                  {'test': test, 'test_id': test_id, 'csrf_token': csrf_token})


class TestDetailView(APIView):
    serializer_class = TestSerializer

    def get(self, request, test_id):
        test = get_object_or_404(Test.objects.prefetch_related('questions__answers'), id=test_id)

        serialized_test = self.serializer_class(test).data

        print(serialized_test)

        return Response(serialized_test, status=status.HTTP_200_OK)

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response({'error': 'Пользователь не аутентифицирован'}, status=status.HTTP_401_UNAUTHORIZED)
        return super().dispatch(request, *args, **kwargs)


