from django.urls import path

from tests.views import take_test, TestDetailView

app_name = 'tests'

urlpatterns = [
    path('test/<int:test_id>/api/v1/', TestDetailView.as_view(), name='test_detail'),
    path('test/<int:test_id>/', take_test, name='take_test'),
]
