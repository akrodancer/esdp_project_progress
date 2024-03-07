from django.urls import path

from online_tests.views import TestPassingView, TestDetailView, TestSubmitView, test_results

app_name = 'online_tests'

urlpatterns = [
    path('test/<int:test_id>/', TestPassingView.as_view(), name='take_test'),
    path('test/<int:test_id>/api/v1/', TestDetailView.as_view(), name='api_test_detail'),
    path('test/<int:test_id>/api/v1/submit', TestSubmitView.as_view(), name='api_save_user_test'),
    path('test/results/<int:user_test_id>/', test_results, name='test_results'),
]
