from django.urls import path
from django.contrib.auth.views import LoginView
from accounts.views import UserRegisterView, UserLogin, logout_view, StudentDetailView, StudentListView, CommentCreateView, SignUpUsersView
app_name = 'accounts'

urlpatterns = [
    path('login/', UserLogin.as_view(), name='log_in'),
    path('logout/', logout_view, name='log_out'),
    path('registration/', UserRegisterView.as_view(), name='user_reg'),
    path('search/', StudentListView.as_view(), name='search_student'),
    path('<int:pk>/', StudentDetailView.as_view(), name='student_detail'),
    path('<int:pk>/comment/', CommentCreateView.as_view(), name='add_comment'),
    path('sign_up/', SignUpUsersView.as_view(), name='sign_up_course'),
]


