from django.urls import path

from online_tests.views import TestPassingView, TestDetailView, submit

app_name = 'online_tests'

urlpatterns = [
    path('test/<int:test_id>/', TestPassingView.as_view(), name='take_test'),
    path('test/<int:test_id>/api/v1/', TestDetailView.as_view(), name='api_test_detail'),
    path('test/<int:test_id>/api/v1/submit', submit, name='api_save_user_test'),
]
