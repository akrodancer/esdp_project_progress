from django.urls import path
from accounts.views import UserRegisterView
app_name = 'accounts'

urlpatterns = [
    path('registration/', UserRegisterView.as_view(), name='user_reg')
]