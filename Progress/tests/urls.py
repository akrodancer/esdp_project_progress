from django.urls import path
from .views import TestView

app_name = 'tests'

urlpatterns = [
    path('', TestView.as_view())
]