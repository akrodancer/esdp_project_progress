from django.urls import path
from courses.views import IndexPageView, AboutUsView, CoursesView

app_name = 'courses'

urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    path('about_us/', AboutUsView.as_view(), name='about_us'),
    path('courses/', CoursesView.as_view(), name='courses'),
]