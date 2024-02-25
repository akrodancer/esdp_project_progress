from django.urls import path
from .views import StudentDetailView, StudentListView

app_name = 'accounts'

urlpatterns = [
    path('search/', StudentListView.as_view(), name='search_student'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student_detail')
]
