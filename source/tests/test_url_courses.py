from django.urls import reverse, resolve
from django.test import TestCase
from courses.views import IndexPageView, AboutUsView, CoursesView, LessonsView


class UrlsTest(TestCase):
    def test_index_page_url_resolves(self):
        url = reverse('courses:index')
        self.assertEquals(resolve(url).func.view_class, IndexPageView)

    def test_about_us_url_resolves(self):
        url = reverse('courses:about_us')
        self.assertEquals(resolve(url).func.view_class, AboutUsView)

    def test_courses_url_resolves(self):
        url = reverse('courses:courses')
        self.assertEquals(resolve(url).func.view_class, CoursesView)

    def test_lessons_url_resolves(self):
        url = reverse('courses:lessons')
        self.assertEquals(resolve(url).func.view_class, LessonsView)
