from django.urls import path

from tests.views import take_test

app_name = 'tests'

urlpatterns = [
    path('test/<int:test_id>/', take_test, name='take_test'),
]
