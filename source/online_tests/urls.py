from django.urls import path

from online_tests.views import take_test

app_name = 'online_tests'

urlpatterns = [
    path('test/<int:test_id>/', take_test, name='take_test'),
]
