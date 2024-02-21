from django.urls import path
from django.contrib.auth.views import LoginView
from accounts.views import UserRegisterView
app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/sign_in.html'), name='log_in'),
    path('registration/', UserRegisterView.as_view(), name='user_reg')
]