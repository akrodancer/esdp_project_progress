from django.urls import path
from django.contrib.auth.views import LoginView
from accounts.views import UserRegisterView, UserLogin, logout_view
app_name = 'accounts'

urlpatterns = [
    path('login/', UserLogin.as_view(), name='log_in'),
    path('logout/', logout_view, name='log_out'),
    path('registration/', UserRegisterView.as_view(), name='user_reg')
]